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
        "## 维度得分",
        "",
        "| 维度 | 得分 | 权重 |  |",
        "| --- | --- | --- | --- |",
        f"| 视觉一致性 | {d['visual']} | {result['weights']['visual']} | `{_bar(d['visual'])}` |",
        f"| 功能一致性 | {d['functional']} | {result['weights']['functional']} | `{_bar(d['functional'])}` |",
        f"| 交互一致性 | {d['interaction']} | {result['weights']['interaction']} | `{_bar(d['interaction'])}` |",
        "",
        "## 视觉指标明细（逐视口）",
        "",
        "| 视口 | SSIM↑ | 像素差异率↓ | pHash距离↓ |",
        "| --- | --- | --- | --- |",
    ]
    for vp, m in result["visual_detail"].items():
        lines.append(f"| {vp} | {m['ssim']} | {m['pixel_diff_ratio']} | {m['phash_distance']} |")

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

    lines += ["", "## 功能覆盖", ""]
    cov = result["coverage"]["detail"]
    lines.append(f"- 元素存在率：{cov['el_ok']}/{cov['el_total']}")
    lines.append(f"- 行为通过率：{cov['bh_ok']}/{cov['bh_total']} 个功能点全通过")
    lines.append(f"- 断言通过率：{cov['assert_ok']}/{cov['assert_total']} 条断言")

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
