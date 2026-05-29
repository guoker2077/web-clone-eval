"""FastAPI 应用 —— 云端交互界面的 API 层 + 复刻产物预览。

职责（无状态，可水平扩）：
  POST /api/jobs              提交 {url, scope_text} → 立即返回 job_id（不阻塞）
  GET  /api/jobs             最近任务列表
  GET  /api/jobs/{id}        单任务状态/分数/阶段
  GET  /api/jobs/{id}/logs   进度日志（前端轮询，支持 after_id 增量）
  GET  /preview/{site_id}/   复刻产物预览（serve dist/，重写绝对 asset 路径）
  GET  /report/{site_id}     评估报告（Markdown 源）
  GET  /                     最小交互 UI

为什么预览要重写 asset 路径：Vite 默认 base="/"，产物 index.html 里引用的是
绝对路径 /assets/xxx.js。我们把每个产物挂在 /preview/<site_id>/ 子路径下，
故需把 index.html 内的 "/assets/" 改写成 "/preview/<site_id>/assets/"。
上云时这步消失——产物直接传对象存储 + 独立域名，天然各占一个 origin。
"""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))

from server import jobstore  # noqa: E402
from ssrf_guard import SSRFError, assert_url_allowed, guard_enabled  # noqa: E402

OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="web-clone-eval cloud", version="0.1")


@app.on_event("startup")
def _startup() -> None:
    jobstore.init_db()


class SubmitReq(BaseModel):
    url: str = Field(..., description="要复刻的网址")
    scope_text: str = Field(..., min_length=1, description="自然语言复刻范围")
    max_rounds: int = Field(2, ge=1, le=5)
    threshold: float = Field(85.0, ge=0, le=100)


@app.post("/api/jobs")
def submit(req: SubmitReq) -> JSONResponse:
    url = req.url.strip()
    # 入口校验。基础：scheme 白名单。开启 SSRF_GUARD 后（云端 web 服务默认开），
    # 进一步解析 DNS 并拦截内网/云元数据/保留段地址——接入公网前的硬门槛。
    if guard_enabled():
        try:
            assert_url_allowed(url)
        except SSRFError as e:
            raise HTTPException(400, str(e))
    elif not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(400, "url 必须以 http:// 或 https:// 开头")
    job = jobstore.create_job(url, req.scope_text.strip(),
                              max_rounds=req.max_rounds, threshold=req.threshold)
    return JSONResponse({"job_id": job["id"], "site_id": job["site_id"],
                         "status": job["status"]}, status_code=201)


@app.get("/api/jobs")
def jobs() -> dict:
    return {"jobs": jobstore.list_jobs()}


@app.get("/api/jobs/{job_id}")
def job_detail(job_id: str) -> dict:
    job = jobstore.get_job(job_id)
    if job is None:
        raise HTTPException(404, "job 不存在")
    site_id = job["site_id"]
    job["has_preview"] = (OUTPUT / site_id / "dist" / "index.html").exists()
    job["has_report"] = (REPORTS / site_id / "report.md").exists()
    return job


@app.get("/api/jobs/{job_id}/logs")
def job_logs(job_id: str, after_id: int = 0) -> dict:
    if jobstore.get_job(job_id) is None:
        raise HTTPException(404, "job 不存在")
    return {"logs": jobstore.get_logs(job_id, after_id=after_id)}


def _safe_dist_file(site_id: str, rel: str) -> Path:
    """把 /preview/<site_id>/<rel> 映射到 output/<site_id>/dist/<rel>，
    并防目录穿越（rel 解析后必须仍在 dist 内）。"""
    dist = (OUTPUT / site_id / "dist").resolve()
    target = (dist / rel).resolve()
    if not str(target).startswith(str(dist)):
        raise HTTPException(403, "非法路径")
    return target


@app.get("/preview/{site_id}/{rel:path}")
def preview(site_id: str, rel: str) -> Response:
    rel = rel or "index.html"
    target = _safe_dist_file(site_id, rel)
    if target.is_dir():
        target = target / "index.html"
    if not target.exists():
        # SPA 兜底：未命中文件时回 index.html
        target = _safe_dist_file(site_id, "index.html")
        if not target.exists():
            raise HTTPException(404, "产物不存在或尚未构建完成")
    # index.html 需把绝对 asset 路径重写到本预览子路径下
    if target.name == "index.html":
        html = target.read_text(encoding="utf-8")
        html = html.replace('src="/', f'src="/preview/{site_id}/')
        html = html.replace('href="/', f'href="/preview/{site_id}/')
        return HTMLResponse(html)
    return FileResponse(target)


@app.get("/report/{site_id}")
def report(site_id: str) -> Response:
    md = REPORTS / site_id / "report.md"
    if not md.exists():
        raise HTTPException(404, "报告不存在")
    return Response(md.read_text(encoding="utf-8"),
                    media_type="text/markdown; charset=utf-8")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse((STATIC / "index.html").read_text(encoding="utf-8"))


# 静态资源（UI 自身的 css/js，如有）
if STATIC.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")
