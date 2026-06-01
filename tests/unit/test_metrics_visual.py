"""视觉度量单测：证明确定性指标「同输入必同输出、可复现」，且语义正确。

这是报告「可置信」论点的代码级背书——确定性指标无采样误差，重复计算结果完全一致。
用程序生成的小图，不依赖任何外部截图或网络。
"""
from __future__ import annotations

import numpy as np
import pytest
from PIL import Image

import metrics_visual as mv


def _write_img(path, color, size=(64, 64)):
    """生成一张纯色小图写到 path。color 为 (R,G,B)。"""
    arr = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    arr[:, :] = color
    Image.fromarray(arr).save(path)
    return str(path)


@pytest.fixture
def same_pair(tmp_path):
    a = _write_img(tmp_path / "a.png", (200, 50, 50))
    b = _write_img(tmp_path / "b.png", (200, 50, 50))  # 与 a 完全相同
    return a, b


@pytest.fixture
def diff_pair(tmp_path):
    a = _write_img(tmp_path / "a.png", (255, 255, 255))  # 纯白
    b = _write_img(tmp_path / "b.png", (0, 0, 0))        # 纯黑（极端不同）
    return a, b


# ── 语义正确性 ──────────────────────────────────────────────────────────

def test_ssim_identical_is_one(same_pair):
    a, b = same_pair
    assert mv.ssim_score(a, b) == pytest.approx(1.0, abs=1e-6)


def test_pixel_diff_identical_is_zero(same_pair):
    a, b = same_pair
    assert mv.pixel_diff_ratio(a, b) == pytest.approx(0.0, abs=1e-9)


def test_phash_identical_is_zero(same_pair):
    a, b = same_pair
    assert mv.phash_distance(a, b) == 0


def test_pixel_diff_opposite_is_max(diff_pair):
    a, b = diff_pair
    # 纯白 vs 纯黑：所有像素都超阈值，差异率应为 1.0
    assert mv.pixel_diff_ratio(a, b) == pytest.approx(1.0, abs=1e-9)


def test_ssim_opposite_is_low(diff_pair):
    a, b = diff_pair
    assert mv.ssim_score(a, b) < 0.1


# ── 可复现性（核心论点）────────────────────────────────────────────────

def test_metrics_are_reproducible(diff_pair):
    """同一对输入重复算 5 次，三个指标必须 bit-for-bit 一致。"""
    a, b = diff_pair
    runs = [(mv.ssim_score(a, b), mv.pixel_diff_ratio(a, b), mv.phash_distance(a, b))
            for _ in range(5)]
    assert len(set(runs)) == 1, f"确定性指标出现波动：{runs}"


# ── scoped_visual 范围对齐与回退 ────────────────────────────────────────

def test_scoped_visual_missing_module_marked_absent(same_pair):
    """复刻页缺对应 box 时，该模块标 present=False，不进 aggregate。"""
    a, b = same_pair
    ref_boxes = {"foo": {"x": 0, "y": 0, "width": 40, "height": 40}}
    res = mv.scoped_visual(a, b, ref_boxes, {})  # 复刻页无任何 box
    assert res["present"] == 0
    assert res["total"] == 1
    assert res["modules"]["foo"]["present"] is False


def test_scoped_visual_present_module_scored(same_pair):
    """双方都有 box 时，模块被打分且计入 aggregate。"""
    a, b = same_pair
    box = {"x": 5, "y": 5, "width": 40, "height": 40}
    res = mv.scoped_visual(a, b, {"foo": box}, {"foo": box})
    assert res["present"] == 1
    assert res["modules"]["foo"]["present"] is True
    # 相同图同区域：SSIM 应接近 1
    assert res["aggregate"]["ssim"] == pytest.approx(1.0, abs=1e-3)


def test_bbox_iou_basic():
    box = {"x": 0, "y": 0, "width": 10, "height": 10}
    assert mv.bbox_iou(box, box) == pytest.approx(1.0)
    far = {"x": 100, "y": 100, "width": 10, "height": 10}
    assert mv.bbox_iou(box, far) == pytest.approx(0.0)
