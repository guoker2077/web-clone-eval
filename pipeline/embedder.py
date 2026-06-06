"""文本 embedding 封装 —— 教训语义检索（RAG）的向量来源。

为什么本地 ONNX 而非远程 API：中转平台 embedding 端点不稳定（503），本地模型契合
项目「离线、确定、可测」的取向。直接用 onnxruntime + tokenizers 加载模型（不依赖
torch，也不依赖 fastembed 那套 HF 缓存布局），模型经 modelscope（国内可靠）预下载。

多语言模型（paraphrase-multilingual-MiniLM-L12-v2, 384 维）——关键：教训用中文写、
scope 模块描述可能中英混杂，必须跨语言语义对齐（「搜索框」↔「query input」），
词法匹配做不到，这正是上 RAG 的真实理由（实测 中↔英 相似度 0.58 > 无关项 0.33）。

健壮性：模型不可用（没下/缺依赖）时 get_embedder() 返回 None，调用方据此优雅降级
到关键词精确匹配——RAG 是增强，绝不让它成为单点故障。
"""
from __future__ import annotations

import os
import threading

MODEL_ID = os.environ.get(
    "EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

_embedder = None
_tried = False
_lock = threading.Lock()


def _resolve_model_dir() -> str | None:
    """定位本地模型目录：优先构建期预下载的缓存，否则用 modelscope 现拉（首次）。"""
    # 构建期预下载落点（见 Dockerfile）：/opt/fastembed-cache/ms/<model_id>
    pre = os.path.join(os.environ.get("FASTEMBED_CACHE_PATH", "/opt/fastembed-cache"),
                       "ms", MODEL_ID)
    if os.path.isfile(os.path.join(pre, "onnx", "model.onnx")):
        return pre
    try:
        from modelscope import snapshot_download
        return snapshot_download(MODEL_ID)
    except Exception:  # noqa: BLE001
        return None


class _Embedder:
    """onnxruntime + tokenizers，mean-pooling + L2 归一化，输出 384 维句向量。"""

    def __init__(self):
        import numpy as np
        import onnxruntime as ort
        from tokenizers import Tokenizer
        self._np = np
        mdir = _resolve_model_dir()
        if not mdir:
            raise RuntimeError("无法定位 embedding 模型")
        self._sess = ort.InferenceSession(
            os.path.join(mdir, "onnx", "model.onnx"),
            providers=["CPUExecutionProvider"])
        self._tok = Tokenizer.from_file(os.path.join(mdir, "tokenizer.json"))
        self._input_names = {i.name for i in self._sess.get_inputs()}

    def embed(self, texts: list[str]):
        np = self._np
        out = []
        for t in texts:
            enc = self._tok.encode(t)
            ids = np.array([enc.ids], dtype=np.int64)
            mask = np.array([enc.attention_mask], dtype=np.int64)
            feeds = {"input_ids": ids, "attention_mask": mask}
            if "token_type_ids" in self._input_names:
                feeds["token_type_ids"] = np.zeros_like(ids)
            last = self._sess.run(None, feeds)[0]              # (1, seq, 384)
            m = mask[..., None].astype("float32")
            v = (last * m).sum(1) / np.clip(m.sum(1), 1e-9, None)  # mean pool
            vec = v[0]
            n = float(np.linalg.norm(vec))
            out.append((vec / n if n else vec).astype("float32"))
        return out


def get_embedder():
    """返回 embedding 单例；不可用时返回 None（调用方降级到关键词匹配）。"""
    global _embedder, _tried
    if _embedder is not None:
        return _embedder
    if _tried:
        return None
    with _lock:
        if _embedder is None and not _tried:
            _tried = True
            try:
                _embedder = _Embedder()
            except Exception as e:  # noqa: BLE001
                print(f"[embedder] 语义模型不可用，降级关键词匹配："
                      f"{type(e).__name__}: {str(e)[:120]}")
                _embedder = None
    return _embedder


def cosine(a, b) -> float:
    """余弦相似度（向量已 L2 归一化时即点积；这里仍按通式算以防万一）。"""
    import numpy as np
    a = np.asarray(a, dtype="float32")
    b = np.asarray(b, dtype="float32")
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))
