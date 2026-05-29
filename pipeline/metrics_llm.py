"""LLM 辅助视觉评分（加分项）：用 Claude 视觉模型按 rubric 交叉验证量化指标。

让模型同时看原页与复刻页截图，按布局/配色/排版/组件四个子项打分(0-100)，
输出结构化 JSON。该分数作为「辅助信号」，与确定性指标(SSIM等)交叉验证，
不参与主总分（因 LLM 评分非确定性），但在报告中并列展示。
"""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path

from config import DEFAULT_MODEL, get_client

RUBRIC = """你是 UI 还原度评审。左图是原始页面，右图是复刻页面。
请按以下四个维度各打 0-100 分，并给一句简短理由：
- layout: 整体布局结构、区块位置、对齐
- color: 配色、主题色、背景/前景对比
- typography: 字体风格、字号层级、文字排版
- components: 关键组件（输入框/按钮/卡片等）样式还原

只输出 JSON，格式：
{"layout": 85, "color": 90, "typography": 80, "components": 88,
 "overall": 86, "comment": "一句话总评"}"""


def _img_block(path: Path, label: str) -> list:
    data = base64.standard_b64encode(path.read_bytes()).decode()
    return [
        {"type": "text", "text": label},
        {"type": "image",
         "source": {"type": "base64", "media_type": "image/png", "data": data}},
    ]


def llm_visual_score(ref_png: Path, clone_png: Path) -> dict:
    """返回 {layout,color,typography,components,overall,comment} 或 {error}。"""
    if not ref_png.exists() or not clone_png.exists():
        return {"error": "截图缺失"}
    content = [{"type": "text", "text": RUBRIC}]
    content += _img_block(ref_png, "【原始页面】")
    content += _img_block(clone_png, "【复刻页面】")

    client = get_client()
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": content}],
        )
        text = "".join(b.text for b in resp.content
                        if getattr(b, "type", "") == "text")
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return {"error": "未解析到 JSON", "raw": text[:200]}
        data = json.loads(m.group(0))
        return data
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {str(e)[:150]}"}


if __name__ == "__main__":
    import sys

    ROOT = Path(__file__).resolve().parent.parent
    site = sys.argv[1]
    ref = ROOT / "output" / site / "_capture" / "desktop.png"
    clone = ROOT / "reports" / site / "clone_desktop.png"
    print(json.dumps(llm_visual_score(ref, clone), ensure_ascii=False, indent=2))
