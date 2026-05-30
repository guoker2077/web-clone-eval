"""把 reports/<site>/eval.json 渲染成可读的 Markdown 评估报告。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _bar(score: float, width: int = 20) -> str:
    filled = int(round(score / 100 * width))
    return "█" * filled + "░" * (width - filled)


def render(site_id: str) -> Path:
    rep_dir = ROOT / "reports" / site_id
    result = json.loads((rep_dir / "eval.json").read_text(encoding="utf-8"))
    scope = json.loads((ROOT / "scopes" / f"{site_id}.json").read_text(encoding="utf-8"))

    d = result["dimensions"]
    lines = [
        f"# 一致性评估报告：{scope['name']}",
        "",
        f"- 原始网址：{scope['url']}",
        f"- 复刻类型：{scope.get('type','-')}",
        f"- **综合得分：{result['score']} / 100**",
        "",
        "> 度量可置信性说明：标注 `确定性` 的指标（SSIM/像素差/pHash/各覆盖率）"
        "为精确计算，同一输入必得同一结果、可复现；标注 `非确定` 的 LLM 视觉分"
        "为辅助信号，不计入主总分，仅用于与确定性指标交叉验证（见下文）。"
        "所有比率均附原始计数（分子/分母），便于核对。",
        "",
        "## 维度得分",
        "",
        "| 维度 | 得分 | 权重 | 性质 |  |",
        "| --- | --- | --- | --- | --- |",
        f"| 视觉一致性 | {d['visual']} | {result['weights']['visual']} | 确定性·可复现 | `{_bar(d['visual'])}` |",
        f"| 功能一致性 | {d['functional']} | {result['weights']['functional']} | 确定性·可复现 | `{_bar(d['functional'])}` |",
        f"| 交互一致性 | {d['interaction']} | {result['weights']['interaction']} | 确定性·可复现 | `{_bar(d['interaction'])}` |",
        "",
        "## 视觉指标明细（逐视口，确定性·可复现）",
        "",
        "| 视口 | SSIM↑ | 像素差异率↓ | pHash距离↓ |",
        "| --- | --- | --- | --- |",
    ]
    for vp, m in result["visual_detail"].items():
        lines.append(f"| {vp} | {m['ssim']} | {m['pixel_diff_ratio']} | {m['phash_distance']} |")

    # 交叉验证：两种独立方法（确定性 vs LLM）的视觉分是否相互印证
    cv = result.get("cross_validation")
    if cv:
        verdict = ("✅ 一致——两种独立方法结论吻合，视觉评分可信"
                   if cv["agree"] else
                   "⚠️ 存疑——两法差距偏大，建议人工复核视觉评分")
        lines += [
            "",
            "## 交叉验证（可置信度）",
            "",
            "> 用两种**独立**方法测同一对象，相互印证：确定性指标（SSIM 等，可复现）"
            "与 LLM 视觉分（非确定，独立视角）。二者接近则结论可信。",
            "",
            f"- 确定性视觉分：**{cv['deterministic_visual']}**",
            f"- LLM 视觉分（均值）：**{cv['llm_visual_avg']}**",
            f"- 差距：**{cv['delta']}**（阈值 {cv['threshold']}）",
            f"- 判定：{verdict}",
        ]

    # LLM 辅助视觉评分（加分项，与确定性指标交叉验证，不计入主总分）
    llm_visual = result.get("llm_visual") or {}
    if any(not v.get("error") for v in llm_visual.values()):
        lines += [
            "",
            "## LLM 辅助视觉评分（交叉验证，不计入主总分）",
            "",
            "> 让 Claude 视觉模型同时看原页与复刻页，按 rubric 打分。评分已对齐"
            "复刻范围：只评 scope 声明的模块，范围外内容缺失不扣分。"
            "因 LLM 评分非确定性，仅作辅助信号与上方确定性指标交叉验证。",
            "",
            "| 视口 | 布局 | 配色 | 排版 | 组件 | 总评 | 点评 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for vp, s in llm_visual.items():
            if s.get("error"):
                lines.append(f"| {vp} | — | — | — | — | — | 评分失败：{s['error']} |")
            else:
                lines.append(
                    f"| {vp} | {s.get('layout','-')} | {s.get('color','-')} | "
                    f"{s.get('typography','-')} | {s.get('components','-')} | "
                    f"**{s.get('overall','-')}** | {s.get('comment','')} |"
                )

        # 逐模块小分（范围对齐 rubric 产出）：定位哪个声明模块没还原好
        mod_lines: list[str] = []
        for vp, s in llm_visual.items():
            for m in (s.get("modules") or []):
                if not isinstance(m, dict):
                    continue
                mod_lines.append(
                    f"| {vp} | {m.get('name','-')} | "
                    f"**{m.get('score','-')}** | {m.get('note','')} |")
        if mod_lines:
            lines += [
                "",
                "### 逐模块还原度（复刻范围内）",
                "",
                "| 视口 | 模块 | 得分 | 说明 |",
                "| --- | --- | --- | --- |",
                *mod_lines,
            ]

    lines += ["", "## 功能覆盖（确定性·可复现）", ""]
    cov = result["coverage"]["detail"]

    def _rate(ok: int, total: int) -> str:
        pct = round(ok / total * 100, 1) if total else 100.0
        return f"{ok}/{total}（{pct}%）"

    lines.append(f"- 元素存在率：{_rate(cov['el_ok'], cov['el_total'])}")
    lines.append(f"- 行为通过率：{_rate(cov['bh_ok'], cov['bh_total'])} 个功能点全通过")
    lines.append(f"- 断言通过率：{_rate(cov['assert_ok'], cov['assert_total'])} 条断言")

    lines += ["", "### 交互断言明细", ""]
    for fid, fb in result["behaviors"]["features"].items():
        mark = "✅" if fb["ok"] else "❌"
        lines.append(f"- {mark} **{fid}** ({fb['passed']}/{fb['total']})")
        for a in fb["asserts"]:
            amark = "✓" if a["ok"] else "✗"
            err = f" — {a.get('error','')}" if not a["ok"] and a.get("error") else ""
            lines.append(f"  - {amark} `{a['step']}`{err}")

    lines += ["", "## 评估结论", ""]
    if result["score"] >= 85:
        verdict = "复刻质量高，核心功能与视觉还原度均达标。"
    elif result["score"] >= 70:
        verdict = "复刻基本可用，主要功能实现，视觉或交互存在可改进项。"
    else:
        verdict = "复刻存在明显差距，建议查看精修历史与失败断言。"
    lines.append(verdict)
    lines += [
        "",
        "> 指标说明：SSIM 为结构相似度(0-1，越高越好)；像素差异率为超阈值像素占比；",
        "> pHash 距离为感知哈希汉明距离(0-64，越低越相似)。所有截图统一缩放后比较，",
        "> 动态区域已按 scope.masks 遮罩。",
        "",
    ]

    out = rep_dir / "report.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[report] 生成 {out}")
    return out


if __name__ == "__main__":
    import sys

    render(sys.argv[1])
