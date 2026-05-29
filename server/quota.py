"""提交闸门：限流 / 在途上限 / 每日总量 —— 防滥用与 Claude 成本失控。

为什么需要：每个 job 都是真金白银的 Claude 调用（合成 + 生成视觉大请求 + LLM 评分
+ 最多 N 轮精修）。对外开放后若不设闸，一个脚本即可把 token 刷爆、把队列灌满。
这里在「入队前」做三道与成本直接相关的检查，计数落 SQLite（上云原样换 Redis 的
原子 INCR + TTL，逻辑不变）。

三道闸（任一超限即拒，返回给前端的消息可直接展示）：
  ① 按 IP 限流   —— 单 IP 每窗口（默认 1h）最多 N 条，挡单点刷量
  ② 全局在途上限 —— 未达终态的 job 总数上限，挡队列被灌爆（背压）
  ③ 每日总量上限 —— 全站每日 job 上限，成本总闸（最后一道）

开关：仅当 QUOTA_GUARD 为真时启用（云端 web 开；本地 CLI/调试默认关）。
"""
from __future__ import annotations

import os
import time

from server import jobstore


class QuotaError(Exception):
    """提交超限。带 HTTP 状态码与可直接回前端的消息。"""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def guard_enabled() -> bool:
    return os.environ.get("QUOTA_GUARD", "").lower() in ("1", "true", "yes", "on")


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def assert_within_quota(client_ip: str) -> None:
    """入队前检查三道闸；未启用直接放行。超限抛 QuotaError。"""
    if not guard_enabled():
        return
    now = time.time()

    ip_window_sec = _int_env("QUOTA_IP_WINDOW_SEC", 3600)
    ip_max = _int_env("QUOTA_IP_MAX", 5)
    active_max = _int_env("QUOTA_ACTIVE_MAX", 20)
    daily_max = _int_env("QUOTA_DAILY_MAX", 200)

    # ② 全局在途上限（背压：队列要先有空位）
    if jobstore.count_active_jobs() >= active_max:
        raise QuotaError(429, f"系统繁忙：在途任务已达上限 {active_max}，请稍后再试")

    # ③ 每日总量上限（成本总闸）
    if jobstore.count_jobs_since(now - 86400) >= daily_max:
        raise QuotaError(429, f"已达每日任务上限 {daily_max}，请明天再试")

    # ① 按 IP 限流（挡单点刷量）
    used = jobstore.count_jobs_by_ip_since(client_ip, now - ip_window_sec)
    if used >= ip_max:
        mins = max(1, ip_window_sec // 60)
        raise QuotaError(
            429, f"提交过于频繁：每 {mins} 分钟最多 {ip_max} 个任务，请稍后再试")
