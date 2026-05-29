"""Capture 阶段：用 Playwright 抓取原始页面的视觉与结构信息。

产出（写入 output/<site>/_capture/）：
  - <viewport>.png          每个视口的整页截图（评估视觉一致性的基准）
  - <viewport>.dom.html     渲染后的 DOM 快照
  - meta.json               配色板 / 字体 / 关键元素 bbox / 页面尺寸
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

# 反爬：用真实浏览器 UA
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def _capture_dir(site_id: str) -> Path:
    d = ROOT / "output" / site_id / "_capture"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _extract_page_meta(page) -> dict:
    """在页面上下文里提取配色、字体、关键元素盒模型。"""
    return page.evaluate(
        """
        () => {
          const result = { colors: {}, fonts: {}, boxes: {} };
          const els = Array.from(document.querySelectorAll('*')).slice(0, 4000);
          const colorCount = {};
          const bgCount = {};
          const fontFamily = {};
          const fontSize = {};
          for (const el of els) {
            const cs = getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            if (rect.width < 2 || rect.height < 2) continue;
            const area = rect.width * rect.height;
            colorCount[cs.color] = (colorCount[cs.color] || 0) + area;
            if (cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)')
              bgCount[cs.backgroundColor] = (bgCount[cs.backgroundColor] || 0) + area;
            fontFamily[cs.fontFamily] = (fontFamily[cs.fontFamily] || 0) + 1;
            fontSize[cs.fontSize] = (fontSize[cs.fontSize] || 0) + 1;
          }
          const topN = (obj, n) => Object.entries(obj)
            .sort((a, b) => b[1] - a[1]).slice(0, n).map(([k]) => k);
          result.colors.text = topN(colorCount, 8);
          result.colors.background = topN(bgCount, 8);
          result.fonts.family = topN(fontFamily, 5);
          result.fonts.size = topN(fontSize, 8);
          return result;
        }
        """
    )


def _element_boxes(page, features: list[dict]) -> dict:
    """对带 selector_hint 的关键元素，抓取其可见 bounding box（用于 IoU 评估）。

    selector_hint 可以是逗号分隔的多个候选选择器，按顺序取第一个可见的。
    """
    boxes = {}
    for feat in features:
        hint = feat.get("selector_hint")
        if not hint:
            continue
        for sel in [s.strip() for s in hint.split(",") if s.strip()]:
            try:
                loc = page.locator(sel).first
                if loc.count() == 0:
                    continue
                box = loc.bounding_box()  # 不可见元素返回 None
                if box and box["width"] > 1 and box["height"] > 1:
                    boxes[feat["id"]] = box
                    break
            except Exception:  # noqa: BLE001
                continue
    return boxes


def capture(scope: dict) -> Path:
    site_id = scope["id"]
    out = _capture_dir(site_id)
    wait = scope.get("wait", {})
    masks = scope.get("masks", [])

    meta: dict = {"site_id": site_id, "url": scope["url"], "viewports": {}}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        for vp in scope["viewports"]:
            ctx = browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                user_agent=UA,
                locale="zh-CN",
            )
            page = ctx.new_page()
            page.goto(scope["url"], wait_until=wait.get("until", "networkidle"), timeout=60000)
            if wait.get("extra_ms"):
                page.wait_for_timeout(wait["extra_ms"])

            # 遮罩动态区域，避免污染视觉 diff
            for m in masks:
                try:
                    page.eval_on_selector_all(
                        m["selector"],
                        "els => els.forEach(e => e.style.visibility='hidden')",
                    )
                except Exception:  # noqa: BLE001
                    pass

            png = out / f"{vp['name']}.png"
            page.screenshot(path=str(png), full_page=True)

            dom = out / f"{vp['name']}.dom.html"
            dom.write_text(page.content(), encoding="utf-8")

            page_meta = _extract_page_meta(page)
            page_meta["boxes"] = _element_boxes(page, scope.get("features", []))
            page_meta["screenshot"] = png.name
            meta["viewports"][vp["name"]] = page_meta

            ctx.close()
        browser.close()

    (out / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[capture] 完成 {site_id}: {out}")
    return out


if __name__ == "__main__":
    import sys

    scope_path = ROOT / "scopes" / f"{sys.argv[1]}.json"
    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    capture(scope)
