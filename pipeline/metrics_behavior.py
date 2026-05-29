"""功能 & 交互一致性度量。

通过 Playwright 在复刻页上执行 scope 里定义的交互步骤，逐断言统计通过率。
复刻页约定用 data-testid="<feature-id>" 标记可测试元素。
还顺带采集 focus/hover 等状态的样式变化，用于交互一致性评估。
"""
from __future__ import annotations

from playwright.sync_api import sync_playwright


def _sel(target: str) -> str:
    """把功能点 id 映射为 data-testid 选择器。"""
    return f'[data-testid="{target}"]'


def run_behaviors(clone_url: str, scope: dict, viewport: dict | None = None) -> dict:
    """在复刻页执行所有 behavior 类功能点，返回逐断言结果。"""
    viewport = viewport or {"width": 1280, "height": 800}
    results: dict = {"features": {}, "elements": {}, "states": {}}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(viewport=viewport, locale="zh-CN")
        page = ctx.new_page()
        page.goto(clone_url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(500)

        # 1) element 类功能点：检查对应 testid 是否存在且可见
        for feat in scope["features"]:
            if feat.get("type", "element") != "element":
                continue
            sel = _sel(feat["id"])
            ok = False
            try:
                loc = page.locator(sel).first
                ok = loc.count() > 0 and (loc.bounding_box() is not None)
            except Exception:  # noqa: BLE001
                ok = False
            results["elements"][feat["id"]] = ok

        # 2) behavior 类功能点：执行步骤序列，逐断言记录
        for feat in scope["features"]:
            if feat.get("type") != "behavior":
                continue
            asserts: list[dict] = []
            for step in feat.get("steps", []):
                asserts.append(_run_step(page, step))
            passed = sum(1 for a in asserts if a["ok"])
            results["features"][feat["id"]] = {
                "asserts": asserts,
                "passed": passed,
                "total": len(asserts),
                "ok": passed == len(asserts) and len(asserts) > 0,
            }

        # 3) 交互状态：只对输入类控件采集 focus 前后样式变化
        #    （按钮/列表无意义的 focus 边框，纳入会污染交互分）
        for feat in scope["features"]:
            if feat.get("type", "element") != "element":
                continue
            sel = _sel(feat["id"])
            try:
                loc = page.locator(sel).first
                if loc.count() == 0 or loc.bounding_box() is None:
                    continue
                tag = loc.evaluate("el => el.tagName.toLowerCase()")
                is_input = tag in ("input", "textarea") or loc.evaluate(
                    "el => el.querySelector('input,textarea') !== null"
                )
                if not is_input:
                    continue
                target = loc
                if tag not in ("input", "textarea"):
                    inner = loc.locator("input,textarea").first
                    if inner.count() > 0:
                        target = inner
                before = target.evaluate(
                    "el => { const c=getComputedStyle(el);"
                    "return c.borderColor+'|'+c.boxShadow+'|'+c.outlineStyle; }"
                )
                loc.focus()
                page.wait_for_timeout(100)
                after = target.evaluate(
                    "el => { const c=getComputedStyle(el);"
                    "return c.borderColor+'|'+c.boxShadow+'|'+c.outlineStyle; }"
                )
                results["states"][feat["id"]] = {
                    "focus_changes_style": before != after
                }
            except Exception:  # noqa: BLE001
                continue

        browser.close()
    return results


def _run_step(page, step: dict) -> dict:
    action = step["action"]
    target = step.get("target", "")
    sel = _sel(target) if target else ""
    label = f"{action}({target}" + (f"={step.get('value')!r}" if "value" in step else "") + ")"
    try:
        if action == "fill":
            page.locator(sel).first.fill(step["value"], timeout=5000)
        elif action == "click":
            page.locator(sel).first.click(timeout=5000)
            page.wait_for_timeout(300)
        elif action == "expect_visible":
            ok = page.locator(sel).first.is_visible(timeout=5000)
            return {"step": label, "ok": bool(ok)}
        elif action == "expect_text":
            txt = page.locator(sel).first.inner_text(timeout=5000)
            return {"step": label, "ok": step.get("value", "") in txt}
        else:
            return {"step": label, "ok": False, "error": f"未知动作 {action}"}
        return {"step": label, "ok": True}
    except Exception as e:  # noqa: BLE001
        return {"step": label, "ok": False, "error": str(e)[:120]}


def coverage_score(results: dict, scope: dict) -> dict:
    """功能点覆盖率：element 存在率 + behavior 通过率。"""
    el_total = len(results["elements"])
    el_ok = sum(1 for v in results["elements"].values() if v)
    bh_total = len(results["features"])
    bh_ok = sum(1 for v in results["features"].values() if v["ok"])

    assert_total = sum(v["total"] for v in results["features"].values())
    assert_ok = sum(v["passed"] for v in results["features"].values())

    return {
        "element_presence": (el_ok / el_total) if el_total else 1.0,
        "behavior_pass": (bh_ok / bh_total) if bh_total else 1.0,
        "assert_pass": (assert_ok / assert_total) if assert_total else 1.0,
        "detail": {"el_ok": el_ok, "el_total": el_total,
                   "bh_ok": bh_ok, "bh_total": bh_total,
                   "assert_ok": assert_ok, "assert_total": assert_total},
    }
