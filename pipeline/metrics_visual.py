"""视觉一致性度量。

输入两张截图（原页 / 复刻页），输出可量化指标：
  - SSIM / MS-SSIM        结构相似度 0-1
  - pixel_diff_ratio      像素差异比例（越低越好）
  - phash_distance        感知哈希汉明距离（越低越好）
  - color_delta_e         主色板 CIEDE2000 平均色差（越低越好）
所有图先统一缩放到同一尺寸再比较。
"""
from __future__ import annotations

import cv2
import imagehash
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def _load_rgb(path: str, size: tuple[int, int] | None = None) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if size:
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return img


def _common_size(a: str, b: str) -> tuple[int, int]:
    ia, ib = cv2.imread(a), cv2.imread(b)
    h = min(ia.shape[0], ib.shape[0])
    w = min(ia.shape[1], ib.shape[1])
    # 控制最大边，避免超大整页图拖慢计算
    scale = min(1.0, 1400 / max(h, w))
    return (max(1, int(w * scale)), max(1, int(h * scale)))


def ssim_score(ref: str, cand: str) -> float:
    size = _common_size(ref, cand)
    a = cv2.cvtColor(_load_rgb(ref, size), cv2.COLOR_RGB2GRAY)
    b = cv2.cvtColor(_load_rgb(cand, size), cv2.COLOR_RGB2GRAY)
    return float(ssim(a, b))


def pixel_diff_ratio(ref: str, cand: str, thresh: int = 30) -> float:
    size = _common_size(ref, cand)
    a = _load_rgb(ref, size).astype(np.int16)
    b = _load_rgb(cand, size).astype(np.int16)
    diff = np.abs(a - b).max(axis=2)
    return float((diff > thresh).mean())


def phash_distance(ref: str, cand: str) -> int:
    ha = imagehash.phash(Image.open(ref))
    hb = imagehash.phash(Image.open(cand))
    return int(ha - hb)


def _hex_to_lab(colors: list[str]) -> list[np.ndarray]:
    """把 rgb/rgba 字符串转成 Lab 色空间向量。"""
    labs = []
    for c in colors:
        nums = [int(x) for x in __import__("re").findall(r"\d+", c)[:3]]
        if len(nums) < 3:
            continue
        bgr = np.uint8([[[nums[2], nums[1], nums[0]]]])
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)[0][0].astype(float)
        labs.append(lab)
    return labs


def _ciede2000(lab1: np.ndarray, lab2: np.ndarray) -> float:
    """CIEDE2000 色差。lab 取值为 OpenCV 8-bit Lab，需先归一化到标准范围。"""
    L1, a1, b1 = lab1[0] * 100 / 255, lab1[1] - 128, lab1[2] - 128
    L2, a2, b2 = lab2[0] * 100 / 255, lab2[1] - 128, lab2[2] - 128
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cbar = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cbar**7 / (Cbar**7 + 25**7 + 1e-12)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp -= 360 * (dhp > 180)
    dhp += 360 * (dhp < -180)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp) / 2)
    Lbarp = (L1 + L2) / 2
    Cbarp = (C1p + C2p) / 2
    hbarp = (h1p + h2p) / 2
    if abs(h1p - h2p) > 180:
        hbarp += 180
    T = (1 - 0.17 * np.cos(np.radians(hbarp - 30))
         + 0.24 * np.cos(np.radians(2 * hbarp))
         + 0.32 * np.cos(np.radians(3 * hbarp + 6))
         - 0.20 * np.cos(np.radians(4 * hbarp - 63)))
    Sl = 1 + (0.015 * (Lbarp - 50) ** 2) / np.sqrt(20 + (Lbarp - 50) ** 2)
    Sc = 1 + 0.045 * Cbarp
    Sh = 1 + 0.015 * Cbarp * T
    dtheta = 30 * np.exp(-(((hbarp - 275) / 25) ** 2))
    Rc = 2 * np.sqrt(Cbarp**7 / (Cbarp**7 + 25**7 + 1e-12))
    Rt = -Rc * np.sin(np.radians(2 * dtheta))
    return float(np.sqrt(
        (dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
        + Rt * (dCp / Sc) * (dHp / Sh)
    ))


def color_delta_e(ref_colors: list[str], cand_colors: list[str]) -> float:
    """两组主色板的平均最小色差：对参考色板每个色，找复刻色板最近色，取均值。"""
    ref_lab = _hex_to_lab(ref_colors)
    cand_lab = _hex_to_lab(cand_colors)
    if not ref_lab or not cand_lab:
        return 100.0
    total = 0.0
    for r in ref_lab:
        total += min(_ciede2000(r, c) for c in cand_lab)
    return total / len(ref_lab)


def bbox_iou(box_a: dict, box_b: dict) -> float:
    """两个 bounding box 的 IoU。box 形如 {x,y,width,height}。"""
    ax1, ay1 = box_a["x"], box_a["y"]
    ax2, ay2 = ax1 + box_a["width"], ay1 + box_a["height"]
    bx1, by1 = box_b["x"], box_b["y"]
    bx2, by2 = bx1 + box_b["width"], by1 + box_b["height"]
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    union = box_a["width"] * box_a["height"] + box_b["width"] * box_b["height"] - inter
    return float(inter / union) if union > 0 else 0.0
