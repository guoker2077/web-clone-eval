"""LLM 辅助视觉评分（加分项）：用 Claude 视觉模型按 rubric 交叉验证量化指标。

让模型同时看原页与复刻页截图，按布局/配色/排版/组件四个子项打分(0-100)，
输出结构化 JSON。该分数作为「辅助信号」，与确定性指标(SSIM等)交叉验证，
不参与主总分（因 LLM 评分非确定性），但在报告中并列展示。

【复刻范围对齐】复刻只针对 scope 里声明的模块，整页评分会因复刻页「缺少
范围外内容」（广告/背景图/推荐卡片/页脚等）而冤枉扣分——生成目标≠评估目标。
故把声明模块注入 rubric：只评这些模块的还原度，范围外的缺失不扣分，并要求
模型给出逐模块小分，便于报告定位哪个模块没还原好。
"""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path

from config import DEFAULT_MODEL, get_client


def scope_modules(scope: dict) -> list[str]:
    """从 scope 提取「可见模块」描述列表，供视觉 rubric 对齐复刻范围。

    优先取 element 类型特征（它们才是可见 UI 模块）；若没有 element 特征，
    退回所有带 desc 的特征，保证 rubric 总能拿到范围信息。
    """
    feats = scope.get("features", []) or []
    els = [f["desc"] for f in feats
           if f.get("type") == "element" and f.get("desc")]
    if els:
        return els
    return [f["desc"] for f in feats if f.get("desc")]


def _build_rubric(modules: list[str] | None) -> str:
    """按是否有声明模块，构造范围对齐 / 整页两种 rubric。"""
    if modules:
        listed = "\n".join(f"  - {m}" for m in modules)
        scope_block = (
            "本次复刻只要求还原以下指定模块（其余区域不在复刻范围内）：\n"
            f"{listed}\n\n"
            "评分规则：\n"
            "- 只评估上述指定模块的还原度，对照原页中对应区域打分。\n"
            "- 不要因复刻页缺少范围之外的内容（广告、背景大图、推荐卡片、"
            "页脚、登录入口等）而扣分。\n"
            "- 若某指定模块在复刻页缺失或明显错位，则相关维度应给低分。\n"
            "- 额外给出逐模块小分（modules 字段），名称沿用上面列出的模块描述。\n"
        )
        modules_field = (
            ',\n "modules": [{"name": "模块描述", "score": 90, "note": "简评"}]')
    else:
        scope_block = "请评估整体页面的还原度。\n"
        modules_field = ""

    return (
        "你是 UI 还原度评审。左图是原始页面，右图是复刻页面。\n\n"
        f"{scope_block}\n"
        "请按以下四个维度各打 0-100 分（聚焦上述范围），并给一句简短理由：\n"
        "- layout: 指定模块的布局结构、区块位置、对齐\n"
        "- color: 指定模块的配色、主题色、背景/前景对比\n"
        "- typography: 指定模块的字体风格、字号层级、文字排版\n"
        "- components: 指定关键组件（输入框/按钮/卡片等）样式还原\n\n"
        "只输出 JSON，格式：\n"
        '{"layout": 85, "color": 90, "typography": 80, "components": 88,\n'
        ' "overall": 86, "comment": "一句话总评"'
        f"{modules_field}}}"
    )


def _img_block(path: Path, label: str) -> list:
    # 超大/超长图先裁剪+缩放（见 metrics_visual.api_image_bytes），避免长内容页
    # 整页截图触发视觉 API 网关 502。
    from metrics_visual import api_image_bytes

    data = base64.standard_b64encode(api_image_bytes(str(path))).decode()
    return [
        {"type": "text", "text": label},
        {"type": "image",
         "source": {"type": "base64", "media_type": "image/png", "data": data}},
    ]


def llm_visual_score(ref_png: Path, clone_png: Path,
                     modules: list[str] | None = None) -> dict:
    """返回 {layout,color,typography,components,overall,comment[,modules]} 或 {error}。

    modules: 复刻范围内的可见模块描述列表。给定则启用范围对齐 rubric——只评这些
    模块、范围外缺失不扣分、并要求逐模块小分；为空则退回整页评分（向后兼容）。
    """
    if not ref_png.exists() or not clone_png.exists():
        return {"error": "截图缺失"}
    rubric = _build_rubric(modules)
    content = [{"type": "text", "text": rubric}]
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
    scope_path = ROOT / "scopes" / f"{site}.json"
    mods = None
    if scope_path.exists():
        mods = scope_modules(json.loads(scope_path.read_text(encoding="utf-8")))
    print(json.dumps(llm_visual_score(ref, clone, mods),
                     ensure_ascii=False, indent=2))
