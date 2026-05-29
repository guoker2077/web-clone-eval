"""Scope 合成：把「URL + 自然语言复刻范围」展开成结构化 scope.json。

这是云端化的前提。云端 UI 只让用户填两样东西——网址、想复刻什么（自然语言）。
但评估环节需要精确的测试规格（selector_hint、behavior steps、masks、断言）。
本模块在两者之间架桥：

  1. 轻量抓取目标页 DOM，提取交互元素清单（真实 tag/id/name/选择器）；
  2. 把「自然语言范围 + 真实元素清单」交给 Claude，合成结构化 features；
  3. 校验输出（schema、action 白名单、behavior target 引用），落盘成 scope.json。

与 capture.py 解耦：这里只做一次轻量 DOM 抓取（不截图、不提色板），
正常流水线的 capture/generate/evaluate 完全不受影响。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

from config import DEFAULT_MODEL, get_client

ROOT = Path(__file__).resolve().parent.parent

# 评估环节（metrics_behavior._run_step）真正支持的动作，合成必须严格落在白名单内
ALLOWED_ACTIONS = {"fill", "click", "expect_visible", "expect_text"}

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# 候选交互元素：表单控件、按钮、链接、以及常见可点击角色
_INTERACTIVE_JS = r"""
() => {
  const wanted = 'input, textarea, select, button, a[href], '
    + '[role=button], [role=link], [role=textbox], [contenteditable=true]';
  const els = Array.from(document.querySelectorAll(wanted));
  const out = [];
  const seen = new Set();
  for (const el of els) {
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) continue;            // 跳过不可见
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const tag = el.tagName.toLowerCase();
    const item = {
      tag,
      type: el.getAttribute('type') || '',
      id: el.id || '',
      name: el.getAttribute('name') || '',
      placeholder: el.getAttribute('placeholder') || '',
      aria: el.getAttribute('aria-label') || '',
      role: el.getAttribute('role') || '',
      href: tag === 'a' ? (el.getAttribute('href') || '') : '',
      testid: el.getAttribute('data-testid') || '',
      text: (el.innerText || el.value || '').trim().slice(0, 40),
    };
    // 生成一个稳妥的候选选择器（优先 id > name > type > tag）
    let sel = tag;
    if (item.id) sel = '#' + CSS.escape(item.id);
    else if (item.name) sel = `${tag}[name="${item.name}"]`;
    else if (item.type) sel = `${tag}[type="${item.type}"]`;
    item.selector = sel;
    const key = item.selector + '|' + item.text;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(item);
    if (out.length >= 60) break;                          // 控制体积
  }
  return { title: document.title, elements: out };
}
"""


def probe_dom(url: str, wait_until: str = "networkidle",
              extra_ms: int = 1200) -> dict:
    """轻量抓取：只取页面标题 + 可交互元素清单（不截图、不存 DOM）。"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(user_agent=UA, locale="zh-CN",
                                  viewport={"width": 1280, "height": 800})
        page = ctx.new_page()
        try:
            page.goto(url, wait_until=wait_until, timeout=60000)
        except Exception:  # noqa: BLE001
            # 退化：networkidle 抓不到就用 domcontentloaded 再试
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        if extra_ms:
            page.wait_for_timeout(extra_ms)
        data = page.evaluate(_INTERACTIVE_JS)
        browser.close()
    return data


def _slugify(url: str) -> str:
    """从 URL 推一个稳妥的 site id（域名主体 + 路径关键段）。"""
    m = re.sub(r"^https?://", "", url.strip().lower())
    m = m.split("?")[0].split("#")[0]
    parts = [p for p in re.split(r"[/.]", m) if p]
    drop = {"www", "com", "cn", "net", "org", "index", "php", "html", "htm"}
    kept = [p for p in parts if p not in drop]
    slug = "-".join(kept[:3]) if kept else "site"
    return re.sub(r"[^a-z0-9-]", "", slug) or "site"


def _build_prompt(url: str, scope_text: str, dom: dict) -> str:
    elems = json.dumps(dom["elements"], ensure_ascii=False, indent=1)
    return f"""你是网页复刻测试规格设计师。用户只给了「网址」和「自然语言复刻范围」，
你要把它展开成结构化的复刻+评估规格（scope）。我已抓取目标页的真实交互元素清单供你参考。

## 目标页
- 网址：{url}
- 页面标题：{dom.get('title','')}

## 用户的复刻范围（自然语言）
{scope_text}

## 目标页真实交互元素清单（从渲染后 DOM 提取，selector 字段是可用的真实选择器）
{elems}

## 你的任务
把复刻范围拆成若干 feature。两类：
- "element"：一个需要复刻并可被定位的关键元素（输入框/按钮/链接/列表等）。
- "behavior"：一段交互流程，由若干 step 组成，最终用断言验证结果。

## 硬性规则（违反则规格无法运行，极重要）
1. behavior 的 step.action **只能**是以下四种之一：
   - "fill"：填入文本，需 target + value
   - "click"：点击，需 target
   - "expect_visible"：断言某元素可见，需 target
   - "expect_text"：断言某元素文本含 value，需 target + value
2. **所有 step 的 target 必须是某个已声明的 element feature 的 id**（不是 CSS 选择器！）。
   复刻页会按 feature id 给元素打 data-testid，评估靠 data-testid 定位。
   翻页场景如需"下一页"，请显式声明一个 id 为 "next-page" 的 element feature。
3. element feature 的 selector_hint 必须来自上面清单的真实 selector（可逗号分隔多个候选，
   按可靠性排序）。绝不要凭空编造选择器。
4. feature id 用小写连字符英文（如 "username"、"search-input"、"submit-button"）。
5. 只输出与用户范围相关的 feature，不要扩展无关元素。
6. masks：列出会污染视觉对比的动态区域（轮播/广告/验证码图片）的 CSS 选择器，没有就给 []。

## 输出格式（只输出 JSON，不要任何解释文字）
{{
  "name": "页面中文名",
  "type": "form 或 content",
  "features": [
    {{"id": "username", "desc": "用户名输入框", "selector_hint": "#login_field, input[name=login]", "type": "element"}},
    {{"id": "login-flow", "desc": "填入用户名密码并点击登录", "type": "behavior",
      "steps": [
        {{"action": "fill", "target": "username", "value": "octocat"}},
        {{"action": "click", "target": "submit-button"}}
      ]}}
  ],
  "masks": [],
  "notes": "一句话说明复刻要点"
}}"""


def validate_scope(scope: dict) -> list[str]:
    """校验合成的 scope，返回问题列表（空列表=通过）。

    重点防三类会让评估跑不起来的错：未知 action、behavior target 引用了
    不存在的 element id、element 缺 selector_hint。
    """
    errs: list[str] = []
    feats = scope.get("features")
    if not isinstance(feats, list) or not feats:
        return ["features 为空或非列表"]

    element_ids = {f.get("id") for f in feats
                   if f.get("type", "element") == "element"}
    seen_ids = set()
    for i, f in enumerate(feats):
        fid = f.get("id")
        if not fid or not isinstance(fid, str):
            errs.append(f"feature[{i}] 缺合法 id")
            continue
        if fid in seen_ids:
            errs.append(f"feature id 重复: {fid}")
        seen_ids.add(fid)
        ftype = f.get("type", "element")
        if ftype == "element":
            if not f.get("selector_hint"):
                errs.append(f"element [{fid}] 缺 selector_hint")
        elif ftype == "behavior":
            steps = f.get("steps")
            if not isinstance(steps, list) or not steps:
                errs.append(f"behavior [{fid}] 缺 steps")
                continue
            for j, s in enumerate(steps):
                act = s.get("action")
                if act not in ALLOWED_ACTIONS:
                    errs.append(f"behavior [{fid}].step[{j}] 非法 action: {act!r}")
                tgt = s.get("target")
                if not tgt:
                    errs.append(f"behavior [{fid}].step[{j}] 缺 target")
                elif tgt not in element_ids:
                    errs.append(
                        f"behavior [{fid}].step[{j}] target {tgt!r} "
                        f"未声明为 element feature（需补一个 id={tgt} 的 element）")
                if act in ("fill", "expect_text") and "value" not in s:
                    errs.append(f"behavior [{fid}].step[{j}] {act} 缺 value")
        else:
            errs.append(f"feature [{fid}] 未知 type: {ftype}")
    return errs


def _extract_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError("模型未返回 JSON")
    return json.loads(m.group(0))


def synthesize_scope(url: str, scope_text: str, site_id: str | None = None,
                     viewports: list | None = None, save: bool = True) -> dict:
    """主入口：URL + 自然语言范围 → 完整 scope dict（默认落盘 scopes/<id>.json）。"""
    site_id = site_id or _slugify(url)
    print(f"[synth] 探测 DOM: {url}")
    dom = probe_dom(url)
    print(f"[synth] 抓到 {len(dom['elements'])} 个交互元素，调用模型合成 scope...")

    prompt = _build_prompt(url, scope_text, dom)
    client = get_client()
    last_errs: list[str] = []
    scope: dict = {}
    # 最多两轮：若校验失败，把错误回灌让模型自修
    for attempt in range(2):
        msg = prompt
        if last_errs:
            msg = prompt + ("\n\n## 上次输出的校验错误（必须修正后重新输出完整 JSON）\n"
                            + "\n".join(f"- {e}" for e in last_errs))
        resp = client.messages.create(
            model=DEFAULT_MODEL, max_tokens=2000,
            messages=[{"role": "user", "content": msg}],
        )
        text = "".join(b.text for b in resp.content
                       if getattr(b, "type", "") == "text")
        try:
            scope = _extract_json(text)
        except Exception as e:  # noqa: BLE001
            last_errs = [f"JSON 解析失败: {e}"]
            continue
        last_errs = validate_scope(scope)
        if not last_errs:
            break
        print(f"[synth] 第{attempt+1}次校验未过: {last_errs}")

    if last_errs:
        raise RuntimeError(f"scope 合成校验失败: {last_errs}")

    # 补齐运行所需的固定字段
    scope.setdefault("id", site_id)
    scope["id"] = site_id
    scope["url"] = url
    scope.setdefault("viewports", viewports or [
        {"name": "desktop", "width": 1280, "height": 800}
    ])
    scope.setdefault("wait", {"until": "networkidle", "extra_ms": 1500})
    scope.setdefault("masks", [])

    if save:
        out = ROOT / "scopes" / f"{site_id}.json"
        out.write_text(json.dumps(scope, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        print(f"[synth] 已写入 {out}")
    return scope


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(
        description="把 URL + 自然语言复刻范围合成为 scopes/<id>.json")
    ap.add_argument("url")
    ap.add_argument("scope_text", help="自然语言复刻范围，如 '复刻用户名/密码输入框和登录按钮'")
    ap.add_argument("--id", default=None, help="站点 id（默认从 URL 推断）")
    args = ap.parse_args()
    s = synthesize_scope(args.url, args.scope_text, site_id=args.id)
    print(json.dumps(s, ensure_ascii=False, indent=2))
