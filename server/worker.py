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
import threading
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from server import jobstore  # noqa: E402

POLL_INTERVAL = float(os.environ.get("WORKER_POLL_SEC", "2.0"))
JOB_TIMEOUT = float(os.environ.get("JOB_TIMEOUT_SEC", "1800"))  # 单 job 墙钟上限

# 并发度：单 worker 进程内并行跑几条 job。每条 job 各跑一条「认领→执行」循环，
# 靠 jobstore.claim_next 的 BEGIN IMMEDIATE 原子认领保证不重复领同一条。
# 默认 1（与历史串行行为一致）。提高它即获得真并发——重活（npm/chromium）都在
# 子进程里，worker 线程只阻塞在 proc.wait()（释放 GIL），故线程即可实现真并行。
# 上限取决于内存：每条 job 峰值约 1~1.5GB（Chromium + npm 构建），16G 机器建议
# 4~6，2核4G 建议 2。设过高会触发 swap 反而更慢。
WORKER_CONCURRENCY = max(1, int(os.environ.get("WORKER_CONCURRENCY", "1")))

# 沙箱模式：subprocess（默认，本地骨架）| docker（每 job 一次性容器，强隔离）
SANDBOX_MODE = os.environ.get("SANDBOX_MODE", "subprocess").lower()
SANDBOX_IMAGE = os.environ.get("SANDBOX_IMAGE", "web-clone-eval:latest")
SANDBOX_MEMORY = os.environ.get("SANDBOX_MEMORY", "2g")
SANDBOX_CPUS = os.environ.get("SANDBOX_CPUS", "2")
SANDBOX_PIDS = os.environ.get("SANDBOX_PIDS", "512")


def _runner_cmd(job_id: str) -> list[str]:
    """构造 runner 调用命令。

    两种模式（SANDBOX_MODE 控制）：
      subprocess（默认）—— 当前 Python 解释器直接跑 runner；轻、零依赖，但与
        worker 同容器、共享内核与资源。配合 runner 内的 setrlimit（JOB_RLIMIT）
        做进程级软隔离。本地骨架与单机部署够用。
      docker —— 每个 job 关进一次性容器：--rm 用后即焚、--memory/--cpus/--pids-limit
        硬限资源、--cap-drop=ALL 去能力、--security-opt no-new-privileges 禁提权。
        强隔离，代价是 worker 需能调宿主 docker（挂 /var/run/docker.sock，本身是
        提权面，生产建议换 rootless docker 或云任务 API）。

    上云时整体替换为云任务 API（Cloud Run Job / Fargate / k8s Job），由平台做
    资源&网络隔离，无需共享 docker daemon。worker/API 逻辑不变。
    """
    if SANDBOX_MODE == "docker":
        # 把队列 DB 与产物目录挂进沙箱容器，使其与 worker 共享同一份数据卷。
        # 这些路径在 compose 里与宿主机 bind-mount 对齐（见 docker-compose.yml）。
        return [
            "docker", "run", "--rm",
            "--memory", SANDBOX_MEMORY,
            "--cpus", SANDBOX_CPUS,
            "--pids-limit", SANDBOX_PIDS,
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "-e", f"JOBS_DB={os.environ.get('JOBS_DB', '/app/data/jobs.db')}",
            "-e", "SSRF_GUARD=1",
            "-e", "JOB_RLIMIT=1",
            "--env-file", str(ROOT / ".env"),
            "-v", f"{ROOT}/data:/app/data",
            "-v", f"{ROOT}/output:/app/output",
            "-v", f"{ROOT}/reports:/app/reports",
            "-v", f"{ROOT}/prompts:/app/prompts",
            "-v", f"{ROOT}/scopes:/app/scopes",
            "-w", "/app",
            SANDBOX_IMAGE,
            "python", "-m", "server.runner", job_id,
        ]
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


def _claim_loop(worker_id: str, slot: int, stop: dict) -> None:
    """单条「认领→执行」循环。多条并行跑即得并发；原子认领保证不重复领同一条。"""
    slot_id = f"{worker_id}#{slot}"   # 每槽独立 id，便于在 job 记录/日志里区分
    while not stop["flag"]:
        job = jobstore.claim_next(slot_id)
        if job is None:
            time.sleep(POLL_INTERVAL)
            continue
        try:
            _run_one(job)
        except Exception as e:  # noqa: BLE001
            jobstore.finish_job(job["id"], status="failed",
                                error=f"worker 异常: {e}")
            print(f"[worker] job {job['id']} worker 层异常: {e}", file=sys.stderr)


def main() -> None:
    worker_id = f"{socket.gethostname()}-{os.getpid()}-{uuid.uuid4().hex[:4]}"
    jobstore.init_db()
    # 启动时把卡死的 running job 退回队列（崩溃恢复）
    n = jobstore.requeue_stale(JOB_TIMEOUT)
    if n:
        print(f"[worker] 退回 {n} 条超时 running job")
    print(f"[worker] {worker_id} 上线，轮询间隔 {POLL_INTERVAL}s，job 超时 {JOB_TIMEOUT}s，"
          f"并发度={WORKER_CONCURRENCY}，沙箱模式={SANDBOX_MODE}")

    stop = {"flag": False}

    def _graceful(signum, frame):  # noqa: ARG001
        print("[worker] 收到停止信号，处理完当前 job 后退出")
        stop["flag"] = True

    signal.signal(signal.SIGINT, _graceful)
    signal.signal(signal.SIGTERM, _graceful)

    # 起 N 条并行循环。各循环独占一个 claim→run 链路，重活在子进程里跑（阻塞在
    # proc.wait 时释放 GIL），故线程足以实现真并行，无需多进程。
    threads = [
        threading.Thread(target=_claim_loop, args=(worker_id, i, stop),
                         name=f"claim-{i}", daemon=True)
        for i in range(WORKER_CONCURRENCY)
    ]
    for t in threads:
        t.start()
    # 主线程留守，让信号处理器能跑；等收到停止信号后所有循环自然收尾。
    try:
        while not stop["flag"]:
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop["flag"] = True
    for t in threads:
        t.join()

    print("[worker] 已退出")


if __name__ == "__main__":
    main()
