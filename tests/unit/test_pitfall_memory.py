"""教训记忆库单测：生命周期 + 防污染 + 信用分配 + 按相关性注入。

这是第二层 agent 记忆的命门——必须证明：候选不注入、≥2 次才生效、客观信号同 run
跨轮可就地生效、注入按相关性筛选、连续无效则退役。全部离线、确定。
"""
from __future__ import annotations

import importlib

import pytest


@pytest.fixture
def mem(tmp_path, monkeypatch):
    """给 pitfall_memory 指一个临时存储文件，每个测试独立。"""
    import pitfall_memory as pm
    importlib.reload(pm)
    monkeypatch.setattr(pm, "MEM_PATH", tmp_path / "pitfalls.json")
    return pm


# ── 生命周期：candidate → active（≥2 次）──────────────────────────────

def test_first_sighting_stays_candidate(mem):
    item = mem.upsert_lesson("code_block", "保留高亮容器", "llm", "run-1")
    assert item["status"] == "candidate"
    assert item["evidence_count"] == 1
    # candidate 不注入
    assert mem.relevant_lessons(["code_block"]) == []


def test_second_run_promotes_to_active(mem):
    mem.upsert_lesson("code_block", "保留高亮容器", "llm", "run-1")
    item = mem.upsert_lesson("code_block", "保留高亮容器", "llm", "run-2")
    assert item["status"] == "active"
    assert item["evidence_count"] == 2
    injected = mem.relevant_lessons(["code_block"])
    assert len(injected) == 1 and injected[0]["lesson"] == "保留高亮容器"


def test_same_run_does_not_double_count(mem):
    """同一个 run 重复上报同一教训，不重复计「不同 run」数。"""
    mem.upsert_lesson("pagination", "翻页要真实可点", "llm", "run-1")
    item = mem.upsert_lesson("pagination", "翻页要真实可点", "llm", "run-1")
    assert item["evidence_count"] == 1
    assert item["status"] == "candidate"


# ── 客观信号同 run 跨轮反复 → 就地满足 ≥2（用户约定的豁免）─────────────

def test_objective_intra_run_repeat_promotes_immediately(mem):
    """build 报错同一 run 跨 2 轮反复，当 run 即可转 active。"""
    item = mem.upsert_lesson("form_validation", "build 失败：缺类型定义",
                             "build", "run-1", intra_run_repeats=2)
    assert item["status"] == "active"
    assert item["evidence_count"] >= 2


def test_subjective_intra_run_repeat_does_not_promote(mem):
    """解释性信号（llm）不享同 run 豁免，跨轮反复仍只算一次。"""
    item = mem.upsert_lesson("card_list", "卡片间距偏大", "llm", "run-1",
                             intra_run_repeats=3)
    assert item["status"] == "candidate"
    assert item["evidence_count"] == 1


# ── 按相关性注入：只取当前 scope 出现的类型 ────────────────────────────

def test_injection_filters_by_relevance(mem):
    mem.upsert_lesson("code_block", "x", "build", "r1", intra_run_repeats=2)
    mem.upsert_lesson("captcha", "y", "build", "r1", intra_run_repeats=2)
    # 当前页只涉及 code_block → 不应注入 captcha 的教训
    got = mem.relevant_lessons(["code_block"])
    assert [l["module_type"] for l in got] == ["code_block"]


def test_render_for_prompt_empty_when_no_active(mem):
    mem.upsert_lesson("code_block", "x", "llm", "r1")   # 仅 candidate
    assert mem.render_for_prompt(["code_block"]) == ""


def test_render_for_prompt_lists_active(mem):
    mem.upsert_lesson("code_block", "保留高亮容器", "build", "r1", intra_run_repeats=2)
    text = mem.render_for_prompt(["code_block"])
    assert "避坑清单" in text and "保留高亮容器" in text


# ── 信用分配 + 退役：连续无效则停止注入 ────────────────────────────────

def test_record_outcome_retires_after_miss_streak(mem):
    item = mem.upsert_lesson("footer", "页脚分栏", "build", "r1", intra_run_repeats=2)
    lid = item["id"]
    assert item["status"] == "active"
    # 连续 miss 达到阈值 → 退役、不再注入
    for _ in range(mem.RETIRE_MISS_STREAK):
        mem.record_outcome("footer", lid, improved=False)
    assert mem.relevant_lessons(["footer"]) == []


def test_record_outcome_hit_resets_streak(mem):
    item = mem.upsert_lesson("footer", "页脚分栏", "build", "r1", intra_run_repeats=2)
    lid = item["id"]
    mem.record_outcome("footer", lid, improved=False)
    mem.record_outcome("footer", lid, improved=True)    # 命中清零连续 miss
    mem.record_outcome("footer", lid, improved=False)
    # 只累计了 1 次连续 miss（中间被 hit 清零），仍 active
    assert len(mem.relevant_lessons(["footer"])) == 1


# ── 语义召回（RAG）：用 mock embedder 验证排序逻辑，不跑真实模型 ──────────

class _StubEmbedder:
    """把文本映射成预设向量，测语义召回的 top-k 排序（确定、离线）。

    表里按「教训写库时编码的文本」(=`module_type: lesson`) 与 query 文本给向量；
    未登记的文本回退到零向量（相似度 0）。
    """
    def __init__(self, table):
        self.table = table

    def embed(self, texts):
        import numpy as np
        return [np.asarray(self.table.get(t, [0.0, 0.0]), dtype="float32")
                for t in texts]


def test_semantic_recall_crosses_types(mem, monkeypatch):
    """语义召回跨类型：query 语义≈登录提交，应把挂在 login_submit 下的教训排在
    footer 之前——即便检索时根本没传 module_types。证明 RAG 跨类型复用。"""
    import embedder as emb
    table = {
        # 写库编码文本：f"{module_type}: {lesson}"
        "login_submit: 登录按钮点击要给 loading 反馈": [0.9, 0.1],   # 近 query
        "footer: 页脚分栏布局":                        [0.0, 1.0],   # 远 query
        "提交按钮交互":                                 [1.0, 0.0],   # query 文本
    }
    monkeypatch.setattr(emb, "get_embedder", lambda: _StubEmbedder(table))

    mem.upsert_lesson("login_submit", "登录按钮点击要给 loading 反馈", "build",
                      "r1", intra_run_repeats=2)
    mem.upsert_lesson("footer", "页脚分栏布局", "build", "r2", intra_run_repeats=2)

    # 注意：module_types 故意传空，证明召回不依赖类型精确匹配，纯靠语义
    got = mem.semantic_relevant_lessons("提交按钮交互", module_types=[], k=5)
    assert got, "应召回到语义相近的教训"
    assert got[0]["module_type"] == "login_submit"      # 最相近排第一
    assert got[0]["_sim"] > (got[-1]["_sim"] if len(got) > 1 else 0)


def test_semantic_recall_falls_back_without_embedder(mem, monkeypatch):
    """embedder 不可用时，语义召回降级到类型精确匹配（不崩、仍可用）。"""
    import embedder as emb
    monkeypatch.setattr(emb, "get_embedder", lambda: None)
    mem.upsert_lesson("pagination", "翻页要真实可点", "build", "r1", intra_run_repeats=2)
    # 降级路径：按类型取，传入 pagination 应拿到，传入无关类型则空
    assert len(mem.semantic_relevant_lessons("x", ["pagination"])) == 1
    assert mem.semantic_relevant_lessons("x", ["footer"]) == []


