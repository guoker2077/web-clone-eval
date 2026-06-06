"""范围对齐评分逻辑单测（不调 Claude API，只测 prompt 构造与模块提取）。

证明 LLM 视觉评分确实「对齐复刻范围」——把声明模块注入 rubric、明确范围外不扣分。
"""
from __future__ import annotations

from metrics_llm import _build_rubric, scope_modules


def test_scope_modules_prefers_elements():
    scope = {"features": [
        {"type": "element", "desc": "搜索框"},
        {"type": "element", "desc": "搜索按钮"},
        {"type": "behavior", "desc": "搜索流程"},  # behavior 不算可见模块
    ]}
    mods = scope_modules(scope)
    assert mods == ["搜索框", "搜索按钮"]


def test_scope_modules_fallback_when_no_elements():
    """没有 element 特征时，退回所有带 desc 的特征，保证 rubric 总有范围信息。"""
    scope = {"features": [{"type": "behavior", "desc": "登录流程"}]}
    assert scope_modules(scope) == ["登录流程"]


def test_scope_modules_empty():
    assert scope_modules({"features": []}) == []
    assert scope_modules({}) == []


def test_rubric_with_modules_is_scope_aligned():
    """有模块时，rubric 必须列出模块、声明范围外不扣分、要求逐模块小分。"""
    r = _build_rubric(["搜索框", "搜索按钮"])
    assert "搜索框" in r and "搜索按钮" in r
    assert "不要因复刻页缺少范围之外的内容" in r
    assert "modules" in r          # 要求逐模块小分字段


def test_rubric_without_modules_is_whole_page():
    """无模块时退回整页 rubric，不含逐模块字段。"""
    r = _build_rubric(None)
    assert "整体页面" in r
    assert "modules" not in r


# ── 用户反馈即时诊断（diagnose_feedback，用 mock client）─────────────────

def test_diagnose_feedback_forces_user_source(monkeypatch):
    """单条反馈提炼出的教训 source 必须强制为 user（不享客观信号豁免）。"""
    import types
    import diagnose as D

    class _Resp:
        content = [types.SimpleNamespace(
            type="text",
            text='[{"module_type": "pagination", "lesson": "翻页要真实可点"}]')]

    class _Client:
        def __init__(self): self.messages = self
        def create(self, **kw): return _Resp()

    monkeypatch.setattr(D, "get_client", lambda: _Client())
    out = D.diagnose_feedback("下一页点了没反应", ["pagination", "search_input"])
    assert len(out) == 1
    assert out[0]["module_type"] == "pagination"
    assert out[0]["source"] == "user"      # 强制标记


def test_diagnose_feedback_empty_returns_empty():
    import diagnose as D
    assert D.diagnose_feedback("   ", ["pagination"]) == []
