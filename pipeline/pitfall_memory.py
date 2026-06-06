"""教训记忆库（agent memory）—— 跨站复用的「模块类型级避坑清单」。

第二层（B 类失败：写完但语义/结构错，尤其复发性问题）。诊断 agent 从一次 run 的
客观信号（build 报错、孤儿 CSS、失败断言）与解释性信号（LLM 逐模块诊断、用户反馈）
里提炼教训，按**规范化模块类型**沉淀；生成前按相关性注入 prompt 当避坑清单。

防污染靠教训的生命周期 + 信用分配：
  candidate（候选，见过 <2 次，不注入）
    → active（生效，独立确认 ≥2 次，注入 prompt）
    → retired（退役，注入后长期无效/被证伪，停止注入）

「独立确认 ≥2 次」的口径（与用户约定）：
  - 客观信号在**同一个 run 内跨多轮反复出现**，就地算满足 ≥2（编译器铁证不浪费）；
  - 否则按**不同 run** 计数。
信用分配：教训是模块类型级，验证也用**该类型模块的逐轮/跨轮评分变化**，把全局归因
缩小成单模块归因（见 record_outcome）。

存储：全局单文件 memory/pitfalls.json。全局存、但**按需取**（注入时只挑当前 scope
出现的类型 + active 的教训），避免 context 膨胀与污染放大。
"""
from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEM_PATH = ROOT / "memory" / "pitfalls.json"

# 转 active 所需的独立确认次数（用户定：一律 ≥2）
PROMOTE_AT = 2
# 注入后连续无效多少次则退役（防一条噪声教训长期误导）
RETIRE_MISS_STREAK = 3

# 信号可信度：客观信号一次确认权重高，解释性信号需更多确认
OBJECTIVE_SOURCES = {"build", "orphan_css", "assertion"}
SUBJECTIVE_SOURCES = {"llm", "user"}


def _load() -> dict:
    if MEM_PATH.exists():
        try:
            return json.loads(MEM_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save(data: dict) -> None:
    MEM_PATH.parent.mkdir(parents=True, exist_ok=True)
    MEM_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                        encoding="utf-8")


def _find(lessons: list[dict], lesson_text: str) -> dict | None:
    """按教训文本在某类型下找已有条目（去重，避免同义教训重复堆积）。"""
    for l in lessons:
        if l.get("lesson", "").strip() == lesson_text.strip():
            return l
    return None


def upsert_lesson(module_type: str, lesson: str, source: str, run_id: str,
                  intra_run_repeats: int = 1) -> dict:
    """新增或确认一条教训，并按生命周期规则更新状态。返回该条目。

    module_type: 规范化模块类型（如 search_input / code_block）。
    source: build|orphan_css|assertion|llm|user（决定可信度权重）。
    run_id: 本次 run 的 site_id，用于「不同 run 计数」去重。
    intra_run_repeats: 该问题在本 run 内跨了几轮反复出现。客观信号且 ≥2 时，
      就地满足「独立确认 ≥2」，当 run 即可转 active（编译器铁证不浪费一轮）。
    """
    data = _load()
    lessons = data.setdefault(module_type, [])
    item = _find(lessons, lesson)
    now = time.time()

    if item is None:
        item = {
            "id": f"{module_type}-{len([x for v in data.values() for x in v]) + 1:03d}",
            "lesson": lesson.strip(),
            "source": source,
            "evidence_count": 0,
            "status": "candidate",
            "hits": 0, "misses": 0, "miss_streak": 0,
            "seen_runs": [],
            "created_at": now,
        }
        lessons.append(item)

    # 计数：同一 run 只贡献一次「不同 run」计数；但客观信号的同 run 跨轮反复，
    # 可就地折算成额外确认（不超过把它一次性顶过 PROMOTE_AT 所需）。
    if run_id not in item["seen_runs"]:
        item["seen_runs"].append(run_id)
        item["evidence_count"] += 1
        if source in OBJECTIVE_SOURCES and intra_run_repeats >= 2:
            # 同 run 跨轮反复：补足到至少满足 PROMOTE_AT（仅客观信号享此豁免）
            item["evidence_count"] = max(item["evidence_count"], PROMOTE_AT)

    item["source"] = source
    item["updated_at"] = now
    # 退役过的教训若再次被独立证据命中，给一次复活机会
    if item["status"] != "retired" and item["evidence_count"] >= PROMOTE_AT:
        item["status"] = "active"
    _save(data)
    return item


def relevant_lessons(module_types: list[str]) -> list[dict]:
    """注入用：只取「当前 scope 出现的类型 ∩ status=active」的教训。

    全局存、按需取——避免把无关的历史坑全塞进 prompt 稀释注意力、放大污染。
    """
    data = _load()
    out: list[dict] = []
    for mt in module_types:
        for l in data.get(mt, []):
            if l.get("status") == "active":
                out.append({**l, "module_type": mt})
    return out


def render_for_prompt(module_types: list[str]) -> str:
    """把相关 active 教训渲染成 prompt 里的「已知避坑清单」段落；无则返回空串。"""
    lessons = relevant_lessons(module_types)
    if not lessons:
        return ""
    lines = ["## 已知避坑清单（历史复发问题，生成时务必规避）"]
    for l in lessons:
        lines.append(f"- [{l['module_type']}] {l['lesson']}")
    return "\n".join(lines) + "\n"


def record_outcome(module_type: str, lesson_id: str, improved: bool) -> None:
    """信用分配：注入某教训后，看「该类型模块」分数有没有改善，记 hit/miss。

    关键——只看该模块类型的分变化，不看总分，把全局信用分配缩成单模块归因
    （这正是教训用模块类型级的红利）。连续多次 miss → 退役。
    """
    data = _load()
    for l in data.get(module_type, []):
        if l.get("id") != lesson_id:
            continue
        if improved:
            l["hits"] = l.get("hits", 0) + 1
            l["miss_streak"] = 0
        else:
            l["misses"] = l.get("misses", 0) + 1
            l["miss_streak"] = l.get("miss_streak", 0) + 1
            if l["miss_streak"] >= RETIRE_MISS_STREAK:
                l["status"] = "retired"
        break
    _save(data)
