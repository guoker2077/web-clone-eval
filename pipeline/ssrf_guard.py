"""SSRF 防御 —— 校验/拦截用户提交的 URL，防止服务端被诱导访问内网与云元数据。

为什么需要：云端要替陌生人用无头浏览器抓任意 URL。若不设防，攻击者可提交
  - http://169.254.169.254/latest/meta-data/...  偷云厂商 IAM 凭证
  - http://localhost:6379 / http://127.0.0.1:...  打内网服务
  - http://10.x / 172.16-31.x / 192.168.x         打内网主机
  - file:///etc/passwd、gopher://…                越权读本地/打协议
这是教科书级 SSRF。本模块提供两类检查，配合网络层（worker 私有子网+出口过滤）
构成纵深防御。

三个接入点（见 README 安全章节）：
  ① 提交时（app.py）：assert_url_allowed(url) —— 主闸门，挡掉明显非法。
  ② 抓取前（capture/probe_dom）：再查一次，并把已解析 IP 回传，防 DNS rebinding。
  ③ 导航中（Playwright route）：guard_route 拦截每一跳请求，挡重定向到内网。

开关：仅当环境变量 SSRF_GUARD 为真时启用（云端 worker/web 打开；本地 CLI 默认
关闭，方便复刻 http://localhost:3000 这类自有开发页）。
"""
from __future__ import annotations

import ipaddress
import os
import socket
from urllib.parse import urlparse

# 只允许这两种 scheme；其余（file/gopher/ftp/data...）一律拒
ALLOWED_SCHEMES = {"http", "https"}

# 允许的对外端口：默认 Web 端口 + 常见 http 端口。挡掉指向内网服务端口（如
# 6379 Redis、3306 MySQL、22 SSH 等）的尝试。可按需放宽。
ALLOWED_PORTS = {80, 443, 8080, 8443, 8000, 3000, 5000}


class SSRFError(ValueError):
    """URL 未通过 SSRF 校验。消息可直接回给前端。"""


def guard_enabled() -> bool:
    return os.environ.get("SSRF_GUARD", "").lower() in ("1", "true", "yes", "on")


def _ip_is_blocked(ip: str) -> bool:
    """判断一个 IP 是否落在禁止访问的网段。"""
    addr = ipaddress.ip_address(ip)
    # 链路本地：含云元数据 169.254.169.254 / fe80::；这是最关键的一条
    if addr.is_link_local:
        return True
    # 私有网段：10/8、172.16/12、192.168/16、fc00::/7
    if addr.is_private:
        return True
    # 环回 127/8、::1
    if addr.is_loopback:
        return True
    # 未指定 0.0.0.0 / ::、组播、保留
    if addr.is_unspecified or addr.is_multicast or addr.is_reserved:
        return True
    # IPv4 映射的 IPv6（::ffff:10.0.0.1 之类）拆出来再判一次
    if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped:
        return _ip_is_blocked(str(addr.ipv4_mapped))
    return False


def resolve_public_ips(host: str) -> list[str]:
    """解析主机名到 IP 列表；任一 IP 命中黑网段即抛 SSRFError。

    返回通过校验的 IP 列表，调用方可把连接 pin 到这些 IP 上以防 DNS rebinding
    （校验与连接之间域名重新解析成内网）。
    """
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as e:
        raise SSRFError(f"无法解析主机名 {host!r}: {e}")
    ips = sorted({info[4][0] for info in infos})
    if not ips:
        raise SSRFError(f"主机名 {host!r} 未解析到任何 IP")
    for ip in ips:
        if _ip_is_blocked(ip):
            raise SSRFError(f"目标 {host!r} 解析到非法地址 {ip}（内网/元数据/保留段），已拒绝")
    return ips


def assert_url_allowed(url: str) -> list[str]:
    """主闸门：校验 URL 合法性。通过返回已解析的公网 IP 列表，否则抛 SSRFError。

    校验项：scheme 白名单 → 必须有 host → 端口白名单 → host 是 IP 时直接判网段，
    是域名时解析后逐个判网段。
    """
    parsed = urlparse(url.strip())
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise SSRFError(f"不允许的 scheme: {parsed.scheme!r}，仅支持 http/https")
    host = parsed.hostname
    if not host:
        raise SSRFError("URL 缺少主机名")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if port not in ALLOWED_PORTS:
        raise SSRFError(f"不允许的端口 {port}（仅允许 {sorted(ALLOWED_PORTS)}）")

    # host 本身就是 IP 字面量：直接判
    try:
        ipaddress.ip_address(host)
        if _ip_is_blocked(host):
            raise SSRFError(f"目标地址 {host} 属内网/元数据/保留段，已拒绝")
        return [host]
    except ValueError:
        pass  # 不是 IP 字面量，按域名解析
    return resolve_public_ips(host)


def guard_route(route, request) -> None:
    """Playwright 路由拦截器：对每一跳导航/资源请求做 SSRF 复检。

    用法：page 所属 context 上
        context.route("**/*", guard_route)
    作用：原始 URL 通过主闸门后，页面可能 30x 重定向到内网，或页面内请求内网资源；
    这里对每个 request 的 URL 再查一次网段，命中则 abort。

    性能：一个页面会发几十上百个子资源请求，每次都 getaddrinfo 会拖慢甚至超时。
    故按 (scheme, host, port) 缓存判定结果——抓取是短命进程（runner 子进程/沙箱
    容器），缓存随进程销毁，不影响"提交→抓取"之间的 rebinding 防御（那道由
    protect_context 的抓取前复检覆盖）。
    """
    from urllib.parse import urlparse
    parsed = urlparse(request.url)
    key = (parsed.scheme, parsed.hostname, parsed.port)
    cached = _ROUTE_CACHE.get(key)
    if cached is None:
        try:
            assert_url_allowed(request.url)
            cached = True
        except SSRFError:
            cached = False
        _ROUTE_CACHE[key] = cached
    if cached:
        route.continue_()
    else:
        route.abort()


_ROUTE_CACHE: dict[tuple, bool] = {}


def protect_context(context, url: str) -> None:
    """给一个 Playwright context 装上 SSRF 防护（抓取层一行接入）。

    仅当 SSRF_GUARD 开启时生效（云端 worker 开、本地 CLI 关）。做两件事：
      ① 抓取前对 url 复检（解析 DNS 防 rebinding，命中黑段直接抛 SSRFError）；
      ② 在 context 上挂 guard_route，拦截后续每一跳请求（防重定向/页面内请求跳内网）。
    """
    if not guard_enabled():
        return
    assert_url_allowed(url)               # 抓取前复检（防 DNS rebinding）
    context.route("**/*", guard_route)    # 逐请求拦截（防重定向到内网）
