"""scope → 规范化模块类型映射单测（注入相关性键，纯逻辑）。"""
from __future__ import annotations

from diagnose_match import scope_module_types


def test_search_scope_maps_to_search_types():
    scope = {"features": [
        {"id": "search-input", "desc": "搜索输入框"},
        {"id": "search-button", "desc": "搜索按钮"},
        {"id": "next-page", "desc": "下一页翻页按钮"},
    ]}
    types = scope_module_types(scope)
    assert "search_input" in types
    assert "search_button" in types
    assert "pagination" in types


def test_login_scope_maps_to_login_types():
    scope = {"features": [
        {"id": "username", "desc": "用户名输入框"},
        {"id": "password", "desc": "密码输入框"},
        {"id": "submit-button", "desc": "Sign in 登录按钮"},
    ]}
    types = scope_module_types(scope)
    assert "login_username" in types
    assert "login_password" in types
    assert "login_submit" in types


def test_unmatched_features_ignored():
    """匹配不到关键词的 feature 不强行归类（免污染）。"""
    scope = {"features": [{"id": "xyzzy", "desc": "某个无法归类的东西"}]}
    assert scope_module_types(scope) == []


def test_empty_scope():
    assert scope_module_types({}) == []
    assert scope_module_types({"features": []}) == []
