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
from metrics_llm import llm_visual_score

ROOT = Path(__file__).resolve().parent.parent

# 各维度权重（透明、可调）
WEIGHTS = {"visual": 0.4, "functional": 0.4, "interaction": 0.2}
# 视觉子指标权重
VISUAL_WEIGHTS = {"ssim": 0.4, "pixel": 0.2, "phash": 0.15, "color": 0.25}


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
    subprocess.run([npm, "install", "--no-audit", "--no-fund",
                    "--registry=https://registry.npmmirror.com"],
                   cwd=site_dir, check=True, capture_output=True, text=True, timeout=600)
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


def screenshot_clone(url: str, scope: dict, out_dir: Path) -> dict:
    """对复刻页按相同视口截图，遮罩同样区域。返回 {viewport: png_path}。"""
    shots = {}
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
            ctx.close()
        browser.close()
    return shots


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
        clone_shots = screenshot_clone(clone_url, scope, rep_dir)

        # 2) 视觉指标（逐视口）
        visual_per_vp = {}
        for vp in scope["viewports"]:
            name = vp["name"]
            ref = str(cap_dir / f"{name}.png")
            cand = clone_shots[name]
            ssim_v = mv.ssim_score(ref, cand)
            pix = mv.pixel_diff_ratio(ref, cand)
            ph = mv.phash_distance(ref, cand)
            ref_colors = (cap_meta["viewports"][name]["colors"]["text"]
                          + cap_meta["viewports"][name]["colors"]["background"])
            # 复刻页配色：临时抓一次（简化：复用截图主色由 phash/ssim 间接覆盖，
            # 这里用原页色板与复刻页色板对比需复刻页 meta，留待 refine 增强）
            visual_per_vp[name] = {
                "ssim": round(ssim_v, 4),
                "pixel_diff_ratio": round(pix, 4),
                "phash_distance": ph,
            }

        # 视觉分：聚合各视口，归一到 0-1
        ssim_avg = sum(v["ssim"] for v in visual_per_vp.values()) / len(visual_per_vp)
        pix_avg = sum(v["pixel_diff_ratio"] for v in visual_per_vp.values()) / len(visual_per_vp)
        ph_avg = sum(v["phash_distance"] for v in visual_per_vp.values()) / len(visual_per_vp)
        visual_score = (
            VISUAL_WEIGHTS["ssim"] * max(0, ssim_avg)
            + VISUAL_WEIGHTS["pixel"] * (1 - min(1, pix_avg))
            + VISUAL_WEIGHTS["phash"] * (1 - min(1, ph_avg / 32))
            + VISUAL_WEIGHTS["color"] * max(0, ssim_avg)  # 色彩占位用 ssim 兜底
        )

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
    llm_visual: dict = {}
    if use_llm:
        for vp in scope["viewports"]:
            name = vp["name"]
            ref_png = cap_dir / f"{name}.png"
            clone_png = Path(clone_shots[name])
            print(f"[eval] LLM 视觉评分 @ {name} ...")
            llm_visual[name] = llm_visual_score(ref_png, clone_png)

    result = {
        "site_id": site_id,
        "score": round(total * 100, 1),
        "dimensions": {
            "visual": round(visual_score * 100, 1),
            "functional": round(functional_score * 100, 1),
            "interaction": round(interaction_score * 100, 1),
        },
        "visual_detail": visual_per_vp,
        "llm_visual": llm_visual,
        "coverage": cov,
        "behaviors": behaviors,
        "weights": WEIGHTS,
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
