"""Job runner —— 单个 job 的执行体（synthesize → run 闭环），进度回写 jobstore。

设计要点：这是一个**独立可执行进程**（`python -m server.runner <job_id>`）。
worker 通过子进程调用它，而不是在 worker 进程内直接 import 跑。这个进程边界
是有意为之——上云时它原地替换成 `docker run <image> python -m server.runner`，
worker、API 完全不用改。今天是子进程，明天是容器，接口一致。

进程内做两件事：
  ① synthesize_scope(url, scope_text, site_id) → 落盘 scopes/<site_id>.json
  ② run(site_id, ...) 跑完整闭环，progress 回调把阶段写进 job_logs
"""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 让 pipeline 模块可被 import（与 CLI 同样的相对导入风格）
sys.path.insert(0, str(ROOT / "pipeline"))

from server import jobstore  # noqa: E402


def _run_job(job_id: str) -> int:
    job = jobstore.get_job(job_id)
    if job is None:
        print(f"[runner] job {job_id} 不存在", file=sys.stderr)
        return 2

    site_id = job["site_id"]
    url = job["url"]
    scope_text = job["scope_text"]

    def progress(stage: str, message: str) -> None:
        jobstore.set_stage(job_id, stage)
        jobstore.add_log(job_id, message, stage=stage)
        print(f"[{stage}] {message}")

    try:
        from synthesize_scope import synthesize_scope
        from run import run

        progress("synthesizing", f"探测 DOM 并合成 scope：{url}")
        synthesize_scope(url, scope_text, site_id=site_id)

        result = run(
            site_id,
            max_rounds=int(job["max_rounds"]),
            threshold=float(job["threshold"]),
            skip_capture=False,
            progress=progress,
        )
        score = result.get("best_score")
        if score is None:
            jobstore.finish_job(job_id, status="failed",
                                error="所有精修轮均失败，无可用产物")
            progress("failed", "所有精修轮均失败")
            return 1

        jobstore.finish_job(job_id, status="done", score=score)
        jobstore.add_log(job_id, f"完成，最佳分数 {score}（round{result.get('best_round')}）",
                         stage="done")
        print(f"[runner] job {job_id} done, score={score}")
        return 0

    except Exception as e:  # noqa: BLE001
        tb = traceback.format_exc()
        jobstore.add_log(job_id, f"异常：{str(e)[:300]}", stage="failed")
        jobstore.finish_job(job_id, status="failed", error=f"{e}\n{tb[-1000:]}")
        print(f"[runner] job {job_id} failed: {e}\n{tb}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python -m server.runner <job_id>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(_run_job(sys.argv[1]))
