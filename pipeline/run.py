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
from typing import Callable

from capture import capture
from evaluate import evaluate
from generate import generate
from metrics_llm import llm_visual_score, scope_modules

ROOT = Path(__file__).resolve().parent.parent

# 进度回调签名：(stage: str, message: str) -> None。默认 no-op，CLI 路径不受影响。
ProgressFn = Callable[[str, str], None]


def _noop(stage: str, message: str) -> None:  # noqa: ARG001
    pass


def build_feedback(result: dict, llm_visual: dict | None = None) -> str:
    """把评估结果转成给 Claude 的针对性修正反馈。

    llm_visual: 可选的 LLM 逐模块视觉诊断（{viewport: {overall, comment, modules:[...]}}）。
    传入后，把「搜索按钮偏右/颜色偏浅」这类具体诊断也写进反馈——比抽象的 SSIM 分
    数对模型有用得多。
    """
    lines = [f"上一轮总分 {result['score']}/100，各维度："]
    d = result["dimensions"]
    lines.append(f"- 视觉 {d['visual']}, 功能 {d['functional']}, 交互 {d['interaction']}")

    # 视觉低分提示
    for vp, m in result["visual_detail"].items():
        if m["ssim"] < 0.7:
            lines.append(f"- [{vp}] 视觉结构相似度偏低 (SSIM={m['ssim']})，"
                         f"像素差异 {m['pixel_diff_ratio']}，请更贴近原页布局与配色。")

    # LLM 逐模块视觉诊断（具体、可操作，比 SSIM 数字有用）
    if llm_visual:
        for vp, s in llm_visual.items():
            if not isinstance(s, dict) or s.get("error"):
                continue
            if s.get("comment"):
                lines.append(f"- [{vp}] 视觉诊断：{s['comment']}")
            for mod in (s.get("modules") or []):
                if isinstance(mod, dict) and mod.get("note") and \
                        isinstance(mod.get("score"), (int, float)) and mod["score"] < 80:
                    lines.append(f"  · 模块「{mod.get('name','?')}」(得分 {mod['score']})："
                                 f"{mod['note']}")

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


def _diagnose(scope: dict, rep_dir: Path) -> dict | None:
    """精修轮专用：对刚评估的复刻页算一次 LLM 逐模块视觉诊断。

    精修循环里 evaluate(use_llm=False) 不算诊断（省成本）；这里在「还有下一轮要修」
    时单独按需算一次，产出具体诊断回灌给下一轮 generate。失败不致命（返回 None，
    反馈退回纯指标版）。复刻页截图复用评估阶段已截好的 reports/<site>/clone_*.png。
    """
    cap_dir = ROOT / "output" / scope["id"] / "_capture"
    modules = scope_modules(scope)
    diag: dict = {}
    try:
        for vp in scope["viewports"]:
            name = vp["name"]
            ref_png = cap_dir / f"{name}.png"
            clone_png = rep_dir / f"clone_{name}.png"
            if ref_png.exists() and clone_png.exists():
                diag[name] = llm_visual_score(ref_png, clone_png, modules)
    except Exception as e:  # noqa: BLE001
        print(f"[run] LLM 诊断失败（不影响精修，退回纯指标反馈）：{str(e)[:120]}")
        return None
    return diag or None


def run(site_id: str, max_rounds: int, threshold: float, skip_capture: bool,
        progress: ProgressFn = _noop) -> dict:
    scope = json.loads((ROOT / "scopes" / f"{site_id}.json").read_text(encoding="utf-8"))
    out = ROOT / "output" / site_id

    if not skip_capture:
        progress("capturing", "抓取原页（多视口截图 + DOM + 配色）")
        capture(scope)

    feedback: str | None = None
    clone_shot: Path | None = None   # 上一轮复刻页截图，精修时回灌做视觉对比
    history = []
    best = None
    best_round = None
    rounds_dir = out / ".rounds"
    rep_dir = ROOT / "reports" / site_id
    for rnd in range(max_rounds):
        print(f"\n===== Round {rnd} =====")
        try:
            progress(f"generating", f"第 {rnd} 轮：Claude 生成复刻工程")
            generate(scope, feedback=feedback, round_no=rnd, clone_shot=clone_shot)
            progress(f"evaluating", f"第 {rnd} 轮：构建 + 截图 + 打分")
            result = evaluate(scope, use_llm=False)
        except Exception as e:  # noqa: BLE001
            print(f"[run] 第 {rnd} 轮失败: {e}")
            progress(f"refining", f"第 {rnd} 轮失败，将回灌反馈重试: {str(e)[:120]}")
            feedback = (f"上一轮生成/构建/运行失败：{str(e)[:300]}。"
                        f"请严格按 ===FILE: 路径=== 格式输出完整工程，确保能 npm build 并正常运行。")
            clone_shot = None   # 失败轮没有可用产物截图
            history.append({"round": rnd, "error": str(e)[:300]})
            continue

        # 快照本轮源码，便于最后恢复最佳轮
        _snapshot_src(out, rounds_dir / f"round{rnd}")
        history.append({"round": rnd, "score": result["score"],
                        "dimensions": result["dimensions"]})
        progress("refining", f"第 {rnd} 轮得分 {result['score']}/100")
        if best is None or result["score"] > best["score"]:
            best = result
            best_round = rnd

        if result["score"] >= threshold:
            print(f"[run] 达标 ({result['score']} >= {threshold})，停止精修。")
            progress("refining", f"达标（{result['score']} ≥ {threshold}），停止精修")
            break

        # 还有下一轮要修：① 回灌本轮复刻页截图做视觉对比；② 算一次 LLM 逐模块
        # 诊断（仅此时算，最后一轮/达标轮不浪费），把具体诊断写进反馈。
        if rnd < max_rounds - 1:
            llm_diag = _diagnose(scope, rep_dir)
            feedback = build_feedback(result, llm_visual=llm_diag)
            shot = rep_dir / "clone_desktop.png"
            clone_shot = shot if shot.exists() else None
        else:
            feedback = build_feedback(result)

    # 恢复最佳轮的产物 + 重新生成最佳轮的报告
    if best_round is not None:
        _restore_src(out, rounds_dir / f"round{best_round}")
        from report import render
        progress("evaluating", f"以最佳轮 round{best_round} 重算并生成报告")
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

    if best is None:
        # 所有轮都失败：没有任何可用产物。明确报失败，别打印「完成」误导。
        errs = [h.get("error") for h in history if h.get("error")]
        last_err = errs[-1] if errs else "未知错误"
        msg = (f"全部 {max_rounds} 轮均失败，无可用产物。最后一轮错误：{last_err}")
        print(f"\n[run] ❌ {msg}")
        progress("failed", msg)
        return {"best_score": None, "best_round": None,
                "history": history, "failed": True}

    print(f"\n[run] 完成。最佳分数: {best['score']} (round{best_round})")

    # 打包可独立运行的交付产物（干净源码 + 已构建 dist + 站点 README）。
    # 此时 output/<site> 已是最佳轮且 dist 为其构建产物，可直接打包。
    deliver_dir = None
    try:
        from deliver import package_deliverable
        deliver_dir = str(package_deliverable(site_id))
    except Exception as e:  # noqa: BLE001
        # 打包失败不该让整个闭环判负（产物/报告已生成），仅告警。
        print(f"[run] ⚠️ 交付产物打包失败（不影响评估结果）: {e}")
        progress("refining", f"交付打包失败: {str(e)[:120]}")

    return {"best_score": best["score"], "best_round": best_round,
            "history": history, "failed": False, "deliverable": deliver_dir}


if __name__ == "__main__":
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("site_id")
    ap.add_argument("--max-rounds", type=int, default=3)
    ap.add_argument("--threshold", type=float, default=85.0)
    ap.add_argument("--skip-capture", action="store_true")
    args = ap.parse_args()
    summary = run(args.site_id, args.max_rounds, args.threshold, args.skip_capture)
    # 全失败无可用产物时以非 0 退出，避免在 CLI/CI 里被误判为成功
    sys.exit(1 if summary.get("failed") else 0)
