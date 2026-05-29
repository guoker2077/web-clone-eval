"""连通性自测：向中转平台发一个最小请求，确认鉴权与模型可用。"""
from __future__ import annotations

import sys

from config import DEFAULT_MODEL, get_client


def main() -> int:
    try:
        client = get_client()
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] 客户端构造失败: {e}")
        return 1

    print(f"[INFO] 使用模型: {DEFAULT_MODEL}")
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=64,
            messages=[{"role": "user", "content": "只回复两个字：连通"}],
        )
        text = "".join(
            block.text for block in resp.content if getattr(block, "type", "") == "text"
        )
        print(f"[OK] API 连通，模型回复: {text.strip()!r}")
        print(f"[OK] usage: in={resp.usage.input_tokens} out={resp.usage.output_tokens}")
        return 0
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] 请求失败: {type(e).__name__}: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
