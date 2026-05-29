"""流水线总控：capture → generate → (build+evaluate) → refine 闭环。

用法：
  python run.py baidu                 # 跑完整闭环
  python run.py baidu --max-rounds 3  # 指定最大精修轮数
  python run.py baidu --threshold 85  # 达标阈值
  python run.py baidu --skip-capture  # 复用已有抓取
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from capture import capture
from evaluate import evaluate
from generate import generate

ROOT = Path(__file__).resolve().parent.parent


def build_feedback(result: dict) -> str:
    """把评估结果转成给 Claude 的针对性修正反馈。"""
    lines = [f"上一轮总分 {result['score']}/100，各维度："]
    d = result["dimensions"]
    lines.append(f"- 视觉 {d['visual']}, 功能 {d['functional']}, 交互 {d['interaction']}")

    # 视觉低分提示
    for vp, m in result["visual_detail"].items():
        if m["ssim"] < 0.7:
            lines.append(f"- [{vp}] 视觉结构相似度偏低 (SSIM={m['ssim']})，"
                         f"像素差异 {m['pixel_diff_ratio']}，请更贴近原页布局与配色。")

    # 失败的交互断言
    for fid, fb in result["behaviors"]["features"].items():
        if not fb["ok"]:
            failed = [a["step"] for a in fb["asserts"] if not a["ok"]]
            lines.append(f"- 功能点 [{fid}] 未通过断言: {failed}。"
                         f"请确认对应元素带正确 data-testid 且交互逻辑可用。")

    # 缺失的元素
    missing = [k for k, v in result["behaviors"]["elements"].items() if not v]
    if missing:
        lines.append(f"- 以下元素缺失或不可见: {missing}，"
                     f"请补上并标注 data-testid=\"<功能点id>\"。")

    return "\n".join(lines)


def _snapshot_src(out: Path, dest: Path) -> None:
    """把当前复刻源码快照到 dest（排除 _capture/node_modules/dist/.rounds）。"""
    import shutil
    skip = {"_capture", "node_modules", "dist", ".rounds"}
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=True)
    for child in out.iterdir():
        if child.name in skip:
            continue
        if child.is_dir():
            shutil.copytree(child, dest / child.name)
        else:
            shutil.copy2(child, dest / child.name)


def _restore_src(out: Path, src: Path) -> None:
    """用快照 src 覆盖 out 的源码（排除受保护目录）。"""
    import shutil
    skip = {"_capture", "node_modules", "dist", ".rounds"}
    for child in out.iterdir():
        if child.name in skip:
            continue
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
        else:
            child.unlink(missing_ok=True)
    for child in src.iterdir():
        if child.is_dir():
            shutil.copytree(child, out / child.name)
        else:
            shutil.copy2(child, out / child.name)


def run(site_id: str, max_rounds: int, threshold: float, skip_capture: bool) -> None:
    scope = json.loads((ROOT / "scopes" / f"{site_id}.json").read_text(encoding="utf-8"))
    out = ROOT / "output" / site_id

    if not skip_capture:
        capture(scope)

    feedback: str | None = None
    history = []
    best = None
    best_round = None
    rounds_dir = out / ".rounds"
    for rnd in range(max_rounds):
        print(f"\n===== Round {rnd} =====")
        try:
            generate(scope, feedback=feedback, round_no=rnd)
            result = evaluate(scope, use_llm=False)
        except Exception as e:  # noqa: BLE001
            print(f"[run] 第 {rnd} 轮失败: {e}")
            feedback = (f"上一轮生成/构建/运行失败：{str(e)[:300]}。"
                        f"请严格按 ===FILE: 路径=== 格式输出完整工程，确保能 npm build 并正常运行。")
            history.append({"round": rnd, "error": str(e)[:300]})
            continue

        # 快照本轮源码，便于最后恢复最佳轮
        _snapshot_src(out, rounds_dir / f"round{rnd}")
        history.append({"round": rnd, "score": result["score"],
                        "dimensions": result["dimensions"]})
        if best is None or result["score"] > best["score"]:
            best = result
            best_round = rnd

        if result["score"] >= threshold:
            print(f"[run] 达标 ({result['score']} >= {threshold})，停止精修。")
            break
        feedback = build_feedback(result)

    # 恢复最佳轮的产物 + 重新生成最佳轮的报告
    if best_round is not None:
        _restore_src(out, rounds_dir / f"round{best_round}")
        from report import render
        evaluate(scope)   # 用最佳产物重算，保证 eval.json/截图与产物一致
        render(site_id)
        print(f"[run] 已恢复最佳轮 round{best_round} 为最终产物。")

    # 落盘运行历史
    rep_dir = ROOT / "reports" / site_id
    rep_dir.mkdir(parents=True, exist_ok=True)
    (rep_dir / "history.json").write_text(
        json.dumps({"history": history, "best_round": best_round,
                    "best_score": best["score"] if best else None},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[run] 完成。最佳分数: {best['score'] if best else 'N/A'} (round{best_round})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("site_id")
    ap.add_argument("--max-rounds", type=int, default=3)
    ap.add_argument("--threshold", type=float, default=85.0)
    ap.add_argument("--skip-capture", action="store_true")
    args = ap.parse_args()
    run(args.site_id, args.max_rounds, args.threshold, args.skip_capture)
