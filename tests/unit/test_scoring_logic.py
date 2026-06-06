"""可置信判定与功能覆盖率单测（纯逻辑，无网络/模型）。

覆盖：
  - evaluate.cross_validation：确定性 vs LLM 两法交叉验证的一致/存疑/缺失判定
  - metrics_behavior.coverage_score：元素存在率/行为通过率/断言通过率计算
"""
from __future__ import annotations

import pytest

from evaluate import CROSS_AGREE_DELTA, cross_validation
from metrics_behavior import coverage_score
from run import build_feedback


# ── cross_validation：可置信核心 ────────────────────────────────────────

def _llm(overall):
    return {"desktop": {"overall": overall, "comment": "x"}}


def test_cross_validation_agree_when_close():
    cv = cross_validation(80.0, _llm(85))
    assert cv is not None
    assert cv["delta"] == pytest.approx(5.0)
    assert cv["agree"] is True


def test_cross_validation_doubt_when_far():
    cv = cross_validation(20.0, _llm(80))
    assert cv["delta"] == pytest.approx(60.0)
    assert cv["agree"] is False


def test_cross_validation_boundary_at_threshold():
    """差距正好等于阈值时判「一致」（<= 边界）。"""
    cv = cross_validation(70.0, _llm(70 + CROSS_AGREE_DELTA))
    assert cv["delta"] == pytest.approx(CROSS_AGREE_DELTA)
    assert cv["agree"] is True


def test_cross_validation_none_when_llm_missing():
    """LLM 分缺失或全是 error → 无从交叉验证，返回 None。"""
    assert cross_validation(80.0, {}) is None
    assert cross_validation(80.0, {"desktop": {"error": "评分失败"}}) is None


def test_cross_validation_averages_multiple_viewports():
    llm = {"desktop": {"overall": 90}, "mobile": {"overall": 70}}
    cv = cross_validation(80.0, llm)
    assert cv["llm_visual_avg"] == pytest.approx(80.0)
    assert cv["agree"] is True


def test_cross_validation_ignores_errored_viewport():
    """有 error 的视口不参与均值，只用有效的。"""
    llm = {"desktop": {"overall": 88}, "mobile": {"error": "截图缺失"}}
    cv = cross_validation(85.0, llm)
    assert cv["llm_visual_avg"] == pytest.approx(88.0)


# ── coverage_score：功能/交互量化 ───────────────────────────────────────

def _results(elements, features):
    return {"elements": elements, "features": features, "states": {}}


def test_coverage_all_pass():
    res = _results(
        elements={"a": True, "b": True},
        features={"flow": {"ok": True, "passed": 3, "total": 3}},
    )
    cov = coverage_score(res, {})
    assert cov["element_presence"] == pytest.approx(1.0)
    assert cov["behavior_pass"] == pytest.approx(1.0)
    assert cov["assert_pass"] == pytest.approx(1.0)
    assert cov["detail"] == {"el_ok": 2, "el_total": 2, "bh_ok": 1,
                             "bh_total": 1, "assert_ok": 3, "assert_total": 3}


def test_coverage_partial():
    res = _results(
        elements={"a": True, "b": False, "c": False},   # 1/3
        features={"f1": {"ok": True, "passed": 2, "total": 2},
                  "f2": {"ok": False, "passed": 1, "total": 3}},  # 行为 1/2、断言 3/5
    )
    cov = coverage_score(res, {})
    assert cov["element_presence"] == pytest.approx(1 / 3)
    assert cov["behavior_pass"] == pytest.approx(0.5)
    assert cov["assert_pass"] == pytest.approx(3 / 5)


def test_coverage_empty_defaults_to_one():
    """无元素/行为时分母为 0，约定返回 1.0（不惩罚未声明项）。"""
    cov = coverage_score(_results({}, {}), {})
    assert cov["element_presence"] == 1.0
    assert cov["behavior_pass"] == 1.0
    assert cov["assert_pass"] == 1.0


# ── build_feedback：精修反馈构造（含 LLM 逐模块诊断回灌）──────────────────

def _eval_result(score=60.0, ssim=0.3):
    return {
        "score": score,
        "dimensions": {"visual": 50, "functional": 70, "interaction": 60},
        "visual_detail": {"desktop": {"ssim": ssim, "pixel_diff_ratio": 0.5}},
        "behaviors": {"features": {}, "elements": {}},
    }


def test_feedback_includes_low_ssim_hint():
    fb = build_feedback(_eval_result(ssim=0.3))
    assert "SSIM" in fb and "视觉结构相似度偏低" in fb


def test_feedback_without_llm_has_no_module_lines():
    fb = build_feedback(_eval_result())
    assert "视觉诊断" not in fb


def test_feedback_injects_llm_diagnosis():
    """传入 LLM 诊断时，整体点评与低分模块的具体 note 应进入反馈。"""
    llm = {"desktop": {
        "overall": 60, "comment": "整体偏简化",
        "modules": [
            {"name": "搜索按钮", "score": 30, "note": "颜色偏浅、位置偏右"},
            {"name": "搜索框", "score": 95, "note": "还原良好"},
        ],
    }}
    fb = build_feedback(_eval_result(), llm_visual=llm)
    assert "整体偏简化" in fb
    assert "搜索按钮" in fb and "颜色偏浅" in fb       # 低分模块进反馈
    assert "搜索框" not in fb                          # 高分(>=80)模块不刷屏


def test_feedback_skips_errored_llm_viewport():
    llm = {"desktop": {"error": "截图缺失"}}
    fb = build_feedback(_eval_result(), llm_visual=llm)
    assert "视觉诊断" not in fb
