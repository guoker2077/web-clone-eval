"""诊断 agent —— run 结束后复盘所有信号，提炼「模块类型级」教训写入记忆库。

输入是一次 run 收集的诊断信号（客观：build 报错 / 孤儿 CSS / 失败断言；解释性：
LLM 逐模块诊断 / 用户反馈）。诊断 agent 做两件事：
  ① 归一化：把每个问题挂到一个**规范化模块类型**标签（复用已有类型词表，避免
     search_box / search_input 这种同义碎片化）；
  ② 提炼：产出一条**跨站可复用、可操作**的教训（不写"baidu 的某某"，而写"这一类
     模块通常要怎样"）。

诊断本身是 LLM 判断，可能判错——所以产出的教训先进 candidate，靠生命周期 +
信用分配（见 pitfall_memory）验证后才转 active 注入。诊断失败不致命（返回 []）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from config import DEFAULT_MODEL, get_client

ROOT = Path(__file__).resolve().parent.parent

# 已知类型词表：诊断时优先复用，避免同义类型碎片化。可随用法增长。
KNOWN_TYPES = [
    "search_input", "search_button", "search_results", "pagination",
    "login_username", "login_password", "login_submit", "captcha",
    "nav_bar", "breadcrumb", "sidebar_toc", "article_body", "code_block",
    "footer", "form_validation", "card_list", "logo",
]

_PROMPT = """你是前端复刻流水线的「诊断专家」。下面是一次网页复刻 run 的问题信号。
请把每个**反复出现或影响较大**的问题，提炼成一条**跨站可复用**的教训。

要求：
1. 给每条教训挂一个**规范化模块类型**（module_type）。优先从已知类型里选：
{known}
   实在没有合适的才新建一个 snake_case 英文标签（尽量通用，别带具体站名）。
2. 教训（lesson）要**可操作、跨站通用**：写「这类模块通常该怎么做/别怎么做」，
   不要写「baidu 的搜索框……」这种绑定具体站点的话。
3. 只保留**结构性/复发性**问题，忽略一次性偶发。最多 6 条。

## 本次 run 的信号
{signals}

只输出 JSON 数组，每个元素 {{"module_type": "...", "lesson": "...",
"source": "build|orphan_css|assertion|llm|user", "intra_run_repeats": <int>}}。
intra_run_repeats = 该问题在本 run 跨了几轮反复出现（无法判断填 1）。"""


def _format_signals(signals: dict) -> str:
    """把收集到的结构化信号渲染成给诊断 agent 的可读文本。"""
    lines: list[str] = []
    if signals.get("build_errors"):
        lines.append("### 构建/生成报错（客观，最高可信）")
        for r, e in signals["build_errors"]:
            lines.append(f"- round{r}: {e[:400]}")
    if signals.get("orphan_css"):
        lines.append("### 孤儿 CSS（客观：写了样式却没被 import，触发兜底补救）")
        for r, files in signals["orphan_css"]:
            lines.append(f"- round{r}: {', '.join(files)}")
    if signals.get("failed_asserts"):
        lines.append("### 失败的交互断言（客观：Playwright 实测未通过）")
        for r, fid, steps in signals["failed_asserts"]:
            lines.append(f"- round{r} 功能点[{fid}]: {steps}")
    if signals.get("missing_elements"):
        lines.append("### 缺失/不可见元素（客观）")
        for r, els in signals["missing_elements"]:
            lines.append(f"- round{r}: {els}")
    if signals.get("llm_low_modules"):
        lines.append("### LLM 逐模块低分诊断（解释性，需更多确认）")
        for r, name, score, note in signals["llm_low_modules"]:
            lines.append(f"- round{r} 模块「{name}」(得分 {score}): {note}")
    if signals.get("user_feedback"):
        lines.append("### 用户反馈（解释性，高价值）")
        for fb in signals["user_feedback"]:
            lines.append(f"- {fb}")
    return "\n".join(lines) if lines else "（无显著问题信号）"


def diagnose_run(signals: dict) -> list[dict]:
    """让诊断 agent 复盘一次 run 的信号，返回提炼出的教训列表（未写库）。"""
    signal_text = _format_signals(signals)
    if signal_text.startswith("（无"):
        return []
    prompt = _PROMPT.format(known=", ".join(KNOWN_TYPES), signals=signal_text)
    client = get_client()
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL, max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content
                        if getattr(b, "type", "") == "text")
        m = re.search(r"\[.*\]", text, re.DOTALL)
        if not m:
            return []
        lessons = json.loads(m.group(0))
        # 基础校验：必须有 module_type 与 lesson
        return [l for l in lessons
                if isinstance(l, dict) and l.get("module_type") and l.get("lesson")]
    except Exception as e:  # noqa: BLE001
        print(f"[diagnose] 诊断失败（不影响主流程）：{type(e).__name__}: {str(e)[:150]}")
        return []


_FEEDBACK_PROMPT = """用户对一次网页复刻产物提了反馈。请把它提炼成可复用的教训。

复刻范围涉及的模块类型（请尽量从中选 module_type）：
{types}

用户反馈：
{feedback}

要求：教训要**跨站通用、可操作**（写「这类模块通常该怎样」，别绑定具体站名）；
module_type 优先用上面列出的类型，没有合适的才从这个清单选：{known}。
只输出 JSON 数组，元素 {{"module_type": "...", "lesson": "..."}}。最多 4 条。"""


def diagnose_feedback(feedback: str, module_types: list[str]) -> list[dict]:
    """把单条用户反馈即时提炼成模块类型级教训（source 固定为 user）。

    供 v2 报告页「提交反馈即时消费」用：不等下次 run，当场把人工信号转成教训候选。
    module_types 来自该站 scope，约束类型选择、提高归类准确度。
    """
    if not feedback.strip():
        return []
    prompt = _FEEDBACK_PROMPT.format(
        types=", ".join(module_types) or "（未知，自行判断）",
        known=", ".join(KNOWN_TYPES), feedback=feedback.strip())
    client = get_client()
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL, max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content
                        if getattr(b, "type", "") == "text")
        m = re.search(r"\[.*\]", text, re.DOTALL)
        if not m:
            return []
        lessons = json.loads(m.group(0))
        out = []
        for l in lessons:
            if isinstance(l, dict) and l.get("module_type") and l.get("lesson"):
                l["source"] = "user"   # 强制标记来源，享受不到客观信号豁免
                out.append(l)
        return out
    except Exception as e:  # noqa: BLE001
        print(f"[diagnose] 反馈诊断失败：{type(e).__name__}: {str(e)[:150]}")
        return []
