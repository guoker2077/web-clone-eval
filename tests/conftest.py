"""pytest 共享夹具与导入路径设置。

让测试能 import pipeline/ 与 server/ 下的模块（与 CLI/服务同样的相对导入风格）。
所有单测均离线、确定、秒级：不联网、不调 Claude API、不需要 token。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
# pipeline 模块按平铺方式 import（import metrics_visual），server 按包 import
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """给 jobstore 指一个临时 SQLite 库，测完即弃，互不污染。"""
    db = tmp_path / "jobs_test.db"
    monkeypatch.setenv("JOBS_DB", str(db))
    # jobstore 在 import 时就读了 JOBS_DB，故需重载模块让其拿到新路径
    import importlib

    from server import jobstore
    importlib.reload(jobstore)
    jobstore.init_db()
    return jobstore
