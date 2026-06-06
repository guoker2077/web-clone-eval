"""任务队列单测：生命周期 + 并发认领原子性（背书并发执行功能）。

claim_next 用 BEGIN IMMEDIATE 原子认领，是「单 worker 多并发循环」正确性的根基——
N 个槽同时抢队列，每条 job 必须只被认领一次。这里用线程并发抢一批 job 来验证。
"""
from __future__ import annotations

import threading


def test_job_lifecycle(tmp_db):
    js = tmp_db
    job = js.create_job("https://example.com", "测试范围", max_rounds=1)
    assert job["status"] == "queued"
    jid = job["id"]

    claimed = js.claim_next("worker-A")
    assert claimed["id"] == jid
    assert claimed["status"] == "running"

    # 已无 queued job，再认领返回 None
    assert js.claim_next("worker-A") is None

    js.finish_job(jid, status="done", score=88.5)
    done = js.get_job(jid)
    assert done["status"] == "done"
    assert done["score"] == 88.5


def test_logs_incremental(tmp_db):
    js = tmp_db
    job = js.create_job("https://example.com", "x", max_rounds=1)
    jid = job["id"]
    js.add_log(jid, "第一条", stage="generating")
    logs = js.get_logs(jid)
    assert any(l["line"] == "第一条" for l in logs)
    last_id = max(l["id"] for l in logs)
    # after_id 增量：拿不到旧日志
    assert js.get_logs(jid, after_id=last_id) == []


def test_concurrent_claim_no_duplicate(tmp_db):
    """核心：10 条 job、8 个线程并发抢，每条 job 必须恰好被认领一次。"""
    js = tmp_db
    N = 10
    for i in range(N):
        js.create_job(f"https://example.com/{i}", "x", max_rounds=1)

    claimed_ids: list[str] = []
    lock = threading.Lock()

    def grab():
        while True:
            job = js.claim_next(f"w-{threading.get_ident()}")
            if job is None:
                return
            with lock:
                claimed_ids.append(job["id"])

    threads = [threading.Thread(target=grab) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # 认领总数 == job 总数，且无重复（关键：原子认领不会把同一条发给两个槽）
    assert len(claimed_ids) == N
    assert len(set(claimed_ids)) == N


def test_active_and_daily_counts(tmp_db):
    """配额计数：在途数 / 当日总量，供配额闸门用。"""
    js = tmp_db
    import time
    j1 = js.create_job("https://example.com/1", "x", max_rounds=1)
    js.create_job("https://example.com/2", "x", max_rounds=1)
    assert js.count_active_jobs() == 2          # 两条都还在队列（未终态）
    js.finish_job(j1["id"], status="done", score=10)
    assert js.count_active_jobs() == 1          # 完成一条
    # 当日总量应为 2（含已完成的）
    assert js.count_jobs_since(time.time() - 3600) == 2


def test_feedback_store_and_list(tmp_db):
    """用户反馈存储：按 job 存、可列出。"""
    js = tmp_db
    job = js.create_job("https://example.com", "x", max_rounds=1)
    jid, sid = job["id"], job["site_id"]
    assert js.list_feedback(jid) == []
    js.add_feedback(jid, sid, "翻页按钮位置不对")
    js.add_feedback(jid, sid, "配色偏暖")
    fb = js.list_feedback(jid)
    assert [f["text"] for f in fb] == ["翻页按钮位置不对", "配色偏暖"]
