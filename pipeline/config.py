"""共享配置与 Claude 客户端构造。

中转平台（nowcoding.ai）用 ANTHROPIC_AUTH_TOKEN + ANTHROPIC_BASE_URL 鉴权；
官方 API 用 ANTHROPIC_API_KEY。本模块兼容两者。
"""
from __future__ import annotations

import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

# 项目根目录 = 本文件上一级
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")


def get_client() -> Anthropic:
    """构造 Anthropic 客户端，自动适配中转 token 或官方 key。"""
    base_url = os.environ.get("ANTHROPIC_BASE_URL") or None
    auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if auth_token:
        # 中转平台：仅用 auth_token 作 Bearer 鉴权。
        # 关键：绝不能同时传 api_key —— SDK 会同时发 X-Api-Key 头，
        # 中转网关读到无效的 X-Api-Key 会直接 401。
        return Anthropic(auth_token=auth_token, base_url=base_url)
    if api_key:
        return Anthropic(api_key=api_key, base_url=base_url)

    raise RuntimeError(
        "未找到鉴权信息：请在 .env 设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY"
    )
