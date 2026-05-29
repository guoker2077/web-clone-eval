"""Job store —— 用 SQLite 同时充当任务队列 + 状态库（本地异步骨架）。

为什么是 SQLite：本地骨架要"零额外服务"就能把异步链路跑通。
WAL 模式 + `BEGIN IMMEDIATE` 原子认领，给了我们真实的队列语义
（多 worker 不会重复领同一个 job）。上云时这层整体替换为
Redis 队列 + Postgres 状态库，但 API/worker 看到的接口不变。

一条 job 的生命周期状态机：
  queued → running → done / failed
running 期间，stage 字段细化为 synthesizing/capturing/generating/
building/evaluating/refining(round k)，配合 log 表做进度流。
"""
from __future__ import annotations

import json
import os
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("JOBS_DB", ROOT / "server" / "jobs.db"))

# 终态：worker 不再处理；非终态可被认领/推进
TERMINAL = {"done", "failed"}


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id           TEXT PRIMARY KEY,
                site_id      TEXT NOT NULL,
                url          TEXT NOT NULL,
                scope_text   TEXT NOT NULL,
                max_rounds   INTEGER NOT NULL DEFAULT 2,
                threshold    REAL NOT NULL DEFAULT 85.0,
                status       TEXT NOT NULL DEFAULT 'queued',
                stage        TEXT NOT NULL DEFAULT 'queued',
                score        REAL,
                error        TEXT,
                client_ip    TEXT,
                created_at   REAL NOT NULL,
                started_at   REAL,
                finished_at  REAL,
                worker       TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status, created_at);

            CREATE TABLE IF NOT EXISTS job_logs (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id  TEXT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
                ts      REAL NOT NULL,
                stage   TEXT,
                line    TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_logs_job ON job_logs(job_id, id);
            """
        )
        # 兼容旧库：早期 jobs 表没有 client_ip 列，补加（已存在则忽略）
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(jobs)")}
        if "client_ip" not in cols:
            conn.execute("ALTER TABLE jobs ADD COLUMN client_ip TEXT")
        # client_ip 列就绪后再建其索引（旧库 ALTER 之后才存在该列）
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_jobs_ip ON jobs(client_ip, created_at)")


def _slug_from_url(url: str) -> str:
    import re
    m = re.sub(r"^https?://", "", url.strip().lower())
    m = m.split("?")[0].split("#")[0]
    parts = [p for p in re.split(r"[/.]", m) if p]
    drop = {"www", "com", "cn", "net", "org", "index", "php", "html", "htm"}
    kept = [p for p in parts if p not in drop]
    slug = "-".join(kept[:3]) if kept else "site"
    return re.sub(r"[^a-z0-9-]", "", slug) or "site"


def create_job(url: str, scope_text: str, *, max_rounds: int = 2,
               threshold: float = 85.0, client_ip: str | None = None) -> dict[str, Any]:
    """建一条 job。site_id 用 slug + job 短 id 命名空间化，避免并发同 URL 互相覆盖。"""
    job_id = uuid.uuid4().hex
    site_id = f"{_slug_from_url(url)}-{job_id[:8]}"
    now = time.time()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO jobs(id, site_id, url, scope_text, max_rounds, threshold,"
            " status, stage, client_ip, created_at)"
            " VALUES(?,?,?,?,?,?,'queued','queued',?,?)",
            (job_id, site_id, url, scope_text, max_rounds, threshold, client_ip, now),
        )
    add_log(job_id, "已入队，等待 worker 认领", stage="queued")
    return get_job(job_id)


def count_jobs_by_ip_since(client_ip: str, since: float) -> int:
    """某 IP 在 since 时间点之后提交的 job 数（按 IP 限流用）。"""
    with _connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE client_ip=? AND created_at>=?",
            (client_ip, since),
        ).fetchone()
    return int(row["n"])


def count_active_jobs() -> int:
    """全局在途（未达终态）job 数（在途上限/队列满判断用）。"""
    with _connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE status NOT IN ('done','failed')"
        ).fetchone()
    return int(row["n"])


def count_jobs_since(since: float) -> int:
    """全站在 since 之后提交的 job 数（每日总量上限用）。"""
    with _connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE created_at>=?", (since,)
        ).fetchone()
    return int(row["n"])


def claim_next(worker: str) -> dict[str, Any] | None:
    """原子认领最早的 queued job：BEGIN IMMEDIATE 拿写锁，避免多 worker 抢同一条。"""
    conn = _connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT id FROM jobs WHERE status='queued' ORDER BY created_at LIMIT 1"
        ).fetchone()
        if row is None:
            conn.execute("COMMIT")
            return None
        job_id = row["id"]
        conn.execute(
            "UPDATE jobs SET status='running', stage='claimed', started_at=?,"
            " worker=? WHERE id=?",
            (time.time(), worker, job_id),
        )
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()
    add_log(job_id, f"被 worker {worker} 认领", stage="claimed")
    return get_job(job_id)


def set_stage(job_id: str, stage: str) -> None:
    with _connect() as conn:
        conn.execute("UPDATE jobs SET stage=? WHERE id=?", (stage, job_id))


def finish_job(job_id: str, *, status: str, score: float | None = None,
               error: str | None = None) -> None:
    assert status in TERMINAL
    with _connect() as conn:
        conn.execute(
            "UPDATE jobs SET status=?, stage=?, score=?, error=?, finished_at=?"
            " WHERE id=?",
            (status, status, score, error, time.time(), job_id),
        )


def add_log(job_id: str, line: str, *, stage: str | None = None) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO job_logs(job_id, ts, stage, line) VALUES(?,?,?,?)",
            (job_id, time.time(), stage, line),
        )


def get_job(job_id: str) -> dict[str, Any] | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    return dict(row) if row else None


def get_logs(job_id: str, after_id: int = 0) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, ts, stage, line FROM job_logs WHERE job_id=? AND id>?"
            " ORDER BY id",
            (job_id, after_id),
        ).fetchall()
    return [dict(r) for r in rows]


def list_jobs(limit: int = 50) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def requeue_stale(running_timeout: float = 1800.0) -> int:
    """把卡死超时的 running job 退回 queued（崩溃恢复）。返回处理条数。"""
    cutoff = time.time() - running_timeout
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id FROM jobs WHERE status='running' AND started_at < ?",
            (cutoff,),
        ).fetchall()
        for r in rows:
            conn.execute(
                "UPDATE jobs SET status='queued', stage='queued', worker=NULL"
                " WHERE id=?", (r["id"],))
    for r in rows:
        add_log(r["id"], "running 超时，退回队列重试", stage="queued")
    return len(rows)


if __name__ == "__main__":
    init_db()
    print(f"jobs db ready at {DB_PATH}")
