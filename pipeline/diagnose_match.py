"""把一个 scope 映射到它涉及的「规范化模块类型」集合 —— 注入教训时的相关性键。

教训按模块类型存储；生成前要知道「当前页涉及哪些类型」，才能只注入相关的、
避免把全局所有坑都塞进 prompt。这里用关键词匹配 feature 的 id/desc → 类型标签，
与 diagnose.KNOWN_TYPES 对齐。匹配不到的 feature 忽略（不强行归类，免污染）。
"""
from __future__ import annotations

# 类型 → 触发关键词（id 或 desc 命中任一即归为该类型）。关键词尽量中英兼顾。
_TYPE_KEYWORDS: dict[str, list[str]] = {
    "search_input": ["search-input", "搜索输入", "搜索框", "query", "search_box"],
    "search_button": ["search-button", "搜索按钮", "搜索提交", "search_btn"],
    "search_results": ["search-results", "结果列表", "结果文案", "result-list", "b_results"],
    "pagination": ["next-page", "翻页", "下一页", "分页", "pagination", "pager"],
    "login_username": ["username", "用户名", "login_field", "account", "邮箱"],
    "login_password": ["password", "密码"],
    "login_submit": ["submit", "登录按钮", "sign in", "signin", "commit"],
    "captcha": ["captcha", "验证码"],
    "nav_bar": ["nav", "导航栏", "导航", "menu", "header"],
    "breadcrumb": ["breadcrumb", "面包屑"],
    "sidebar_toc": ["toc", "大纲", "侧边栏", "sidebar", "on this page"],
    "article_body": ["article", "正文", "content-", "文章"],
    "code_block": ["code", "代码块", "代码", "pre", "highlight"],
    "footer": ["footer", "页脚", "底部"],
    "form_validation": ["validation", "必填", "校验", "empty"],
    "card_list": ["card", "卡片", "列表"],
    "logo": ["logo", "标志"],
}


def scope_module_types(scope: dict) -> list[str]:
    """返回 scope 涉及的规范化模块类型（去重、有序）。匹配不到的 feature 跳过。"""
    types: list[str] = []
    feats = scope.get("features", []) or []
    blob_parts = []
    for f in feats:
        blob_parts.append(str(f.get("id", "")).lower())
        blob_parts.append(str(f.get("desc", "")).lower())
        blob_parts.append(str(f.get("selector_hint", "")).lower())
    blob = " ".join(blob_parts)
    for mtype, kws in _TYPE_KEYWORDS.items():
        if any(kw.lower() in blob for kw in kws):
            types.append(mtype)
    return types
