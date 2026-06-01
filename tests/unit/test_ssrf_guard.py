"""SSRF 防御单测：证明内网/云元数据/非法 scheme 被拦、正常公网 URL 放行。

全部用 IP 字面量或本地构造，**不触发真实 DNS 解析**（除一处显式标注），离线可跑。
背书报告「安全加固」卖点。
"""
from __future__ import annotations

import pytest

from ssrf_guard import SSRFError, _ip_is_blocked, assert_url_allowed


# ── IP 网段判定 ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("ip", [
    "169.254.169.254",   # 云元数据（最关键）
    "127.0.0.1",         # 环回
    "10.0.0.5",          # 私有 10/8
    "172.16.3.4",        # 私有 172.16/12
    "192.168.1.1",       # 私有 192.168/16
    "0.0.0.0",           # 未指定
    "::1",               # IPv6 环回
])
def test_blocked_ips(ip):
    assert _ip_is_blocked(ip) is True


@pytest.mark.parametrize("ip", [
    "8.8.8.8",           # 公网 DNS
    "1.1.1.1",           # 公网
    "93.184.216.34",     # example.com 段（公网）
])
def test_public_ips_allowed(ip):
    assert _ip_is_blocked(ip) is False


def test_ipv4_mapped_ipv6_blocked():
    """::ffff:10.0.0.1 这种 IPv4 映射地址要拆出内网 IP 再判。"""
    assert _ip_is_blocked("::ffff:10.0.0.1") is True


# ── URL 主闸门 ──────────────────────────────────────────────────────────

def test_reject_non_http_scheme():
    for url in ["file:///etc/passwd", "gopher://x", "ftp://h/f"]:
        with pytest.raises(SSRFError):
            assert_url_allowed(url)


def test_reject_missing_host():
    with pytest.raises(SSRFError):
        assert_url_allowed("http://")


def test_reject_internal_port():
    """指向内网服务端口（6379 Redis 等）应被端口白名单拦下。"""
    with pytest.raises(SSRFError):
        assert_url_allowed("http://1.1.1.1:6379/")


def test_reject_metadata_ip_literal():
    with pytest.raises(SSRFError):
        assert_url_allowed("http://169.254.169.254/latest/meta-data/")


def test_reject_loopback_literal():
    with pytest.raises(SSRFError):
        assert_url_allowed("http://127.0.0.1:8000/")


def test_allow_public_ip_literal():
    """公网 IP + 允许端口：放行并返回该 IP。"""
    assert assert_url_allowed("http://1.1.1.1/") == ["1.1.1.1"]
    assert assert_url_allowed("https://8.8.8.8:443/path") == ["8.8.8.8"]
