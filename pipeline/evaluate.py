"""Evaluate 阶段：构建复刻工程 → 起静态服务 → 截图 → 三维量化打分。

输出 reports/<site>/eval.json + 差异可视化图。
总分 = 视觉 * w_v + 功能 * w_f + 交互 * w_i（权重在 WEIGHTS，透明可调）。
"""
from __future__ import annotations

import json
import socket
import subprocess
import time
from contextlib import closing
from pathlib import Path

from playwright.sync_api import sync_playwright

import metrics_visual as mv
from metrics_behavior import coverage_score, run_behaviors
from metrics_llm import llm_visual_score, scope_modules

ROOT = Path(__file__).resolve().parent.parent

# 各维度权重（透明、可调）
WEIGHTS = {"visual": 0.4, "functional": 0.4, "interaction": 0.2}
# 视觉子指标权重
VISUAL_WEIGHTS = {"ssim": 0.4, "pixel": 0.2, "phash": 0.15, "color": 0.25}

# 交叉验证一致性阈值：两种独立方法（确定性 vs LLM）视觉分差距 ≤ 此值判「一致」
CROSS_AGREE_DELTA = 15.0


def cross_validation(det_visual: float, llm_visual: dict) -> dict | None:
    """确定性视觉分 vs LLM 视觉分的交叉验证。

    可置信的核心不是给单次确定性计算编个「置信度」（那是假精度——SSIM 等是
    精确计算，无采样误差），而是用两种独立方法相互印证：
      - 确定性：SSIM/像素差/pHash，可复现、无随机性
      - LLM：视觉模型按 rubric 打分，非确定性、独立视角
    二者接近 → 结论可信；差距大 → 标「存疑」，提示人工复核。返回 None 表示
    LLM 分缺失（无从交叉验证）。
    """
    overalls = [s["overall"] for s in llm_visual.values()
                if isinstance(s, dict) and not s.get("error")
                and isinstance(s.get("overall"), (int, float))]
    if not overalls:
        return None
    llm_avg = sum(overalls) / len(overalls)
    delta = abs(det_visual - llm_avg)
    return {
        "deterministic_visual": round(det_visual, 1),
        "llm_visual_avg": round(llm_avg, 1),
        "delta": round(delta, 1),
        "agree": delta <= CROSS_AGREE_DELTA,
        "threshold": CROSS_AGREE_DELTA,
    }


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def build_clone(site_dir: Path) -> Path:
    """npm install && 构建，返回构建产物目录 dist/。

    若 `npm run build`（可能含 tsc 类型检查）失败，回退到 `npx vite build`，
    用 esbuild 直接转译，跳过类型检查 —— 目标是产出可运行产物。
    """
    npm = "npm"
    print(f"[eval] npm install @ {site_dir}")
    inst = subprocess.run([npm, "install", "--no-audit", "--no-fund",
                           "--registry=https://registry.npmmirror.com"],
                          cwd=site_dir, capture_output=True, text=True, timeout=600)
    if inst.returncode != 0:
        # 把 npm 的真实报错带出来，否则上层只看到「exit status 1」无从排查
        raise RuntimeError(
            "npm install 失败 (exit "
            f"{inst.returncode}):\n{(inst.stderr or inst.stdout)[-1000:]}"
        )
    print("[eval] npm run build")
    r = subprocess.run([npm, "run", "build"], cwd=site_dir,
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print("[eval] npm run build 失败，回退 npx vite build（跳过类型检查）")
        r2 = subprocess.run(["npx", "vite", "build"], cwd=site_dir,
                            capture_output=True, text=True, timeout=300)
        if r2.returncode != 0:
            raise RuntimeError(
                "构建失败。npm build stderr:\n" + r.stderr[-800:]
                + "\nvite build stderr:\n" + r2.stderr[-800:]
            )
    dist = site_dir / "dist"
    if not dist.exists():
        raise RuntimeError("构建后未找到 dist/ 目录")
    return dist


def serve(dist: Path, port: int) -> subprocess.Popen:
    proc = subprocess.Popen(
        ["python", "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=dist, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    # 等端口起来
    for _ in range(50):
        with closing(socket.socket()) as s:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                break
        time.sleep(0.1)
    return proc


def screenshot_clone(url: str, scope: dict, out_dir: Path) -> tuple[dict, dict]:
    """对复刻页按相同视口截图，并抓取声明模块的 bounding box（用于范围对齐视觉比对）。

    返回 (shots, boxes)：
      shots: {viewport: png_path}
      boxes: {viewport: {feature_id: {x,y,width,height}}}  复刻页元素以 data-testid 定位
    """
    shots: dict = {}
    boxes: dict = {}
    feat_ids = [f["id"] for f in scope.get("features", [])
                if f.get("type", "element") == "element"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        for vp in scope["viewports"]:
            ctx = browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                locale="zh-CN",
            )
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(800)
            png = out_dir / f"clone_{vp['name']}.png"
            page.screenshot(path=str(png), full_page=True)
            shots[vp["name"]] = str(png)
            vp_boxes: dict = {}
            for fid in feat_ids:
                try:
                    loc = page.locator(f'[data-testid="{fid}"]').first
                    if loc.count() == 0:
                        continue
                    box = loc.bounding_box()
                    if box and box["width"] > 1 and box["height"] > 1:
                        vp_boxes[fid] = box
                except Exception:  # noqa: BLE001
                    continue
            boxes[vp["name"]] = vp_boxes
            ctx.close()
        browser.close()
    return shots, boxes


def evaluate(scope: dict, use_llm: bool = True) -> dict:
    site_id = scope["id"]
    site_dir = ROOT / "output" / site_id
    cap_dir = site_dir / "_capture"
    rep_dir = ROOT / "reports" / site_id
    rep_dir.mkdir(parents=True, exist_ok=True)
    cap_meta = json.loads((cap_dir / "meta.json").read_text(encoding="utf-8"))

    # 1) 构建 + 起服务
    dist = build_clone(site_dir)
    port = _free_port()
    proc = serve(dist, port)
    clone_url = f"http://127.0.0.1:{port}/"
    try:
        clone_shots, clone_boxes = screenshot_clone(clone_url, scope, rep_dir)

        # 2) 视觉指标（逐视口）：范围对齐为主、整页为参考
        #    整页比对会被范围外内容（壁纸/资讯流/页脚）拉低，不公平；故主分用
        #    逐声明模块裁剪比对（scoped），整页指标仅作参考留档。
        visual_per_vp = {}
        scoped_per_vp = {}
        for vp in scope["viewports"]:
            name = vp["name"]
            ref = str(cap_dir / f"{name}.png")
            cand = clone_shots[name]
            # 整页（参考）
            visual_per_vp[name] = {
                "ssim": round(mv.ssim_score(ref, cand), 4),
                "pixel_diff_ratio": round(mv.pixel_diff_ratio(ref, cand), 4),
                "phash_distance": mv.phash_distance(ref, cand),
            }
            # 范围对齐（主分）：原页 box 来自 capture，复刻页 box 来自 data-testid
            ref_boxes = cap_meta["viewports"][name].get("boxes", {})
            scoped_per_vp[name] = mv.scoped_visual(
                ref, cand, ref_boxes, clone_boxes.get(name, {}))

        # 视觉分：优先用范围对齐聚合；若某视口无可比模块则该视口回退整页指标
        def _vp_visual(name: str) -> float:
            sc = scoped_per_vp[name]
            src = sc["aggregate"] if sc["present"] > 0 else visual_per_vp[name]
            ssim_v = src["ssim"]
            pix = src["pixel_diff_ratio"]
            ph = src["phash_distance"]
            return (
                VISUAL_WEIGHTS["ssim"] * max(0, ssim_v)
                + VISUAL_WEIGHTS["pixel"] * (1 - min(1, pix))
                + VISUAL_WEIGHTS["phash"] * (1 - min(1, ph / 32))
                + VISUAL_WEIGHTS["color"] * max(0, ssim_v)  # 色彩占位用 ssim 兜底
            )

        visual_score = sum(_vp_visual(vp["name"]) for vp in scope["viewports"]) \
            / len(scope["viewports"])

        # 3) 功能 + 交互指标
        behaviors = run_behaviors(clone_url, scope)
        cov = coverage_score(behaviors, scope)
        # 功能：元素齐备 + 端到端行为是否整体跑通
        functional_score = 0.5 * cov["element_presence"] + 0.5 * cov["behavior_pass"]
        # 交互：操作流程逐断言通过率为主(0.7)，输入控件 focus 状态反馈为辅(0.3)
        state_vals = [s.get("focus_changes_style", False)
                      for s in behaviors["states"].values()]
        focus_ratio = (sum(state_vals) / len(state_vals)) if state_vals else None
        if focus_ratio is None:
            interaction_score = cov["assert_pass"]
        else:
            interaction_score = 0.7 * cov["assert_pass"] + 0.3 * focus_ratio

    finally:
        proc.terminate()

    total = (WEIGHTS["visual"] * visual_score
             + WEIGHTS["functional"] * functional_score
             + WEIGHTS["interaction"] * interaction_score)

    # LLM 辅助视觉评分（加分项，非确定性）：逐视口让模型交叉验证，
    # 不计入主总分，仅作辅助信号在报告中并列展示。
    # 传入复刻范围内的可见模块 → 范围对齐评分（范围外缺失不扣分 + 逐模块小分）。
    llm_visual: dict = {}
    if use_llm:
        modules = scope_modules(scope)
        for vp in scope["viewports"]:
            name = vp["name"]
            ref_png = cap_dir / f"{name}.png"
            clone_png = Path(clone_shots[name])
            print(f"[eval] LLM 视觉评分 @ {name} ...")
            llm_visual[name] = llm_visual_score(ref_png, clone_png, modules)

    result = {
        "site_id": site_id,
        "score": round(total * 100, 1),
        "dimensions": {
            "visual": round(visual_score * 100, 1),
            "functional": round(functional_score * 100, 1),
            "interaction": round(interaction_score * 100, 1),
        },
        "visual_detail": visual_per_vp,
        "scoped_visual_detail": scoped_per_vp,
        "llm_visual": llm_visual,
        "coverage": cov,
        "behaviors": behaviors,
        "weights": WEIGHTS,
        # 可置信度元信息：标注各指标性质（可复现 / 非确定）+ 两法交叉验证
        "metric_nature": {
            "deterministic": ["ssim", "pixel_diff_ratio", "phash_distance",
                              "element_presence", "behavior_pass", "assert_pass"],
            "non_deterministic": ["llm_visual"],
            "note": "确定性指标同输入必同输出、可复现；LLM 视觉分非确定，仅作辅助交叉验证。",
        },
        "cross_validation": cross_validation(
            round(visual_score * 100, 1), llm_visual),
    }
    (rep_dir / "eval.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[eval] {site_id} 总分 {result['score']} "
          f"(视觉 {result['dimensions']['visual']} / "
          f"功能 {result['dimensions']['functional']} / "
          f"交互 {result['dimensions']['interaction']})")
    return result


if __name__ == "__main__":
    import sys

    scope = json.loads((ROOT / "scopes" / f"{sys.argv[1]}.json").read_text(encoding="utf-8"))
    evaluate(scope)
