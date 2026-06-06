"""生成阶段单测：截断续写逻辑 + 多文件解析（不调 Claude API，用 mock client）。

证明 max_tokens 截断时能用 prefill 续写无缝补全，且 assistant 前缀不带尾随空白
（Anthropic API 的硬性约束）。
"""
from __future__ import annotations

import types

import generate as G


class _Resp:
    """模拟 client.messages.create 的返回：一段文本 + 一个 stop_reason。"""
    def __init__(self, text, stop_reason):
        self.content = [types.SimpleNamespace(type="text", text=text)]
        self.stop_reason = stop_reason


class _MockClient:
    """按预设脚本依次返回 (text, stop_reason)，并记录每次收到的 messages。"""
    def __init__(self, script):
        self._script = list(script)
        self.calls = []
        self.messages = self  # 让 client.messages.create 可用

    def create(self, *, model, max_tokens, messages, **kwargs):
        self.calls.append(messages)
        text, stop = self._script.pop(0)
        return _Resp(text, stop)


def test_continuation_concatenates_until_complete():
    """第一次截断、第二次写完：最终文本应为两段拼接。"""
    client = _MockClient([
        ("===FILE: a.txt===\nhel", "max_tokens"),
        ("lo world", "end_turn"),
    ])
    text, stop = G._complete_with_continuation(client, [{"type": "text", "text": "x"}])
    assert stop == "end_turn"
    assert text == "===FILE: a.txt===\nhel" + "lo world"
    # 第二次调用必须带 assistant prefill（续写而非重来）
    assert len(client.calls) == 2
    assert client.calls[1][1]["role"] == "assistant"


def test_continuation_prefill_has_no_trailing_whitespace():
    """assistant 前缀不能以空白结尾（否则 Anthropic API 报错）。"""
    client = _MockClient([
        ("partial line\n  ", "max_tokens"),   # 故意以空白结尾
        ("rest", "end_turn"),
    ])
    text, stop = G._complete_with_continuation(client, [{"type": "text", "text": "x"}])
    prefill = client.calls[1][1]["content"]
    assert prefill == prefill.rstrip(), "prefill 不应有尾随空白"
    # 但累加文本仍保留原始空白，不丢字符
    assert text == "partial line\n  " + "rest"


def test_continuation_stops_at_max_cont():
    """一直截断时，最多续写 max_cont 次后收手（不无限循环）。"""
    # 5 段都 max_tokens，max_cont=2 → 总共最多 1+2=3 次调用
    client = _MockClient([("x", "max_tokens")] * 5)
    text, stop = G._complete_with_continuation(
        client, [{"type": "text", "text": "x"}], max_cont=2)
    assert stop == "max_tokens"
    assert len(client.calls) == 3


def test_no_continuation_when_complete_first_time():
    client = _MockClient([("===FILE: a===\ndone", "end_turn")])
    text, stop = G._complete_with_continuation(client, [{"type": "text", "text": "x"}])
    assert stop == "end_turn"
    assert len(client.calls) == 1


# ── 多文件解析（_parse_files）──────────────────────────────────────────

def test_parse_files_basic():
    text = "===FILE: package.json===\n{\"name\":\"x\"}\n===FILE: src/App.tsx===\nexport {}\n"
    files = G._parse_files(text)
    assert set(files) == {"package.json", "src/App.tsx"}
    assert files["package.json"].strip() == '{"name":"x"}'


def test_parse_files_strips_code_fences():
    text = "===FILE: a.ts===\n```ts\nconst a=1\n```\n"
    files = G._parse_files(text)
    assert "```" not in files["a.ts"]
    assert "const a=1" in files["a.ts"]
