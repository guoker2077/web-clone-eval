"""Worker —— 轮询队列，认领 job，以独立子进程跑 runner，回写状态与日志。

为什么子进程而非 import 调用：
  ① 隔离——一个 job 把进程跑崩（OOM、段错误、Playwright 卡死）不影响 worker；
  ② 超时——可以对整个 job 设墙钟上限，到点直接杀子进程（成本加固的第一道）；
  ③ 上云迁移——把 `[python, -m, server.runner, job_id]` 换成
     `[docker, run, --rm, <限制参数>, image, python, -m, server.runner, job_id]`
     即可把每个 job 关进一次性沙箱容器，worker 逻辑零改动。

本地骨架默认单 worker、串行跑（并发上限=1）。要并发只需起多个 worker 进程，
SQLite 的 BEGIN IMMEDIATE 认领保证不会重复领同一条 job。
"""
from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from server import jobstore  # noqa: E402

POLL_INTERVAL = float(os.environ.get("WORKER_POLL_SEC", "2.0"))
JOB_TIMEOUT = float(os.environ.get("JOB_TIMEOUT_SEC", "1800"))  # 单 job 墙钟上限


def _runner_cmd(job_id: str) -> list[str]:
    """构造 runner 调用命令。

    上云时这里整体替换为 docker run（带 --network、--memory、--cpus、--read-only
    等沙箱/限额参数），其余逻辑不变。本地骨架直接用当前 Python 解释器跑。
    """
    return [sys.executable, "-m", "server.runner", job_id]


def _run_one(job: dict) -> None:
    job_id = job["id"]
    log_f = ROOT / "server" / "worker_logs"
    log_f.mkdir(parents=True, exist_ok=True)
    out_path = log_f / f"{job_id}.log"

    print(f"[worker] 开始 job {job_id} (site={job['site_id']})")
    with open(out_path, "w", encoding="utf-8") as fp:
        proc = subprocess.Popen(
            _runner_cmd(job_id), cwd=ROOT,
            stdout=fp, stderr=subprocess.STDOUT,
            # 新进程组，超时时可整组杀掉（含 npm/playwright 子进程）
            start_new_session=True,
        )
        try:
            proc.wait(timeout=JOB_TIMEOUT)
        except subprocess.TimeoutExpired:
            jobstore.add_log(job_id, f"超过墙钟上限 {JOB_TIMEOUT}s，终止", stage="failed")
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                time.sleep(3)
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            # runner 被杀来不及落终态，这里补一刀
            cur = jobstore.get_job(job_id)
            if cur and cur["status"] not in jobstore.TERMINAL:
                jobstore.finish_job(job_id, status="failed",
                                    error=f"job 执行超时（>{JOB_TIMEOUT}s）")
            return

    # runner 正常退出但万一没落终态（异常路径），兜底标记
    cur = jobstore.get_job(job_id)
    if cur and cur["status"] not in jobstore.TERMINAL:
        rc = proc.returncode
        jobstore.finish_job(job_id, status="failed",
                            error=f"runner 退出码 {rc}，未落终态")


def main() -> None:
    worker_id = f"{socket.gethostname()}-{os.getpid()}-{uuid.uuid4().hex[:4]}"
    jobstore.init_db()
    # 启动时把卡死的 running job 退回队列（崩溃恢复）
    n = jobstore.requeue_stale(JOB_TIMEOUT)
    if n:
        print(f"[worker] 退回 {n} 条超时 running job")
    print(f"[worker] {worker_id} 上线，轮询间隔 {POLL_INTERVAL}s，job 超时 {JOB_TIMEOUT}s")

    stop = {"flag": False}

    def _graceful(signum, frame):  # noqa: ARG001
        print("[worker] 收到停止信号，处理完当前 job 后退出")
        stop["flag"] = True

    signal.signal(signal.SIGINT, _graceful)
    signal.signal(signal.SIGTERM, _graceful)

    while not stop["flag"]:
        job = jobstore.claim_next(worker_id)
        if job is None:
            time.sleep(POLL_INTERVAL)
            continue
        try:
            _run_one(job)
        except Exception as e:  # noqa: BLE001
            jobstore.finish_job(job["id"], status="failed",
                                error=f"worker 异常: {e}")
            print(f"[worker] job {job['id']} worker 层异常: {e}", file=sys.stderr)

    print("[worker] 已退出")


if __name__ == "__main__":
    main()
