"""把闭环选出的最佳轮，打包成「可独立运行的交付产物」。

为什么单独一步：require.md 验收要「完整可长期维护的源码」+「可独立运行的产物/
访问地址」。output/<site> 是带 node_modules/dist/.rounds 的工作目录，不适合直接
交付。这里产出干净的 deliverables/<site>/：

  deliverables/<site>/
    source/        干净源码（React+TS+Vite 工程，去掉 node_modules/dist/.rounds/
                   _capture），可长期维护、可重新构建
    dist/          已构建的静态产物（index.html+assets），零依赖，任意静态服务器
                   或直接打开即可运行——这就是「可独立运行的访问产物」
    README.md      该站点的复刻说明、运行方式、评分摘要、mock 数据声明

交付目录是纯静态/源码快照，不含密钥与抓取中间产物，可直接随仓库提交或上传部署。
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 源码快照排除项：依赖、构建产物、轮次快照、抓取中间产物
# 源码快照排除项：依赖、构建产物、轮次快照、抓取中间产物、内部 sidecar
_SKIP = {"node_modules", "dist", ".rounds", "_capture", ".last_orphans.json"}


def _copy_source(src_dir: Path, dest: Path) -> None:
    """复制干净源码到 dest（排除 _SKIP）。"""
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=True)
    for child in src_dir.iterdir():
        if child.name in _SKIP:
            continue
        if child.is_dir():
            shutil.copytree(child, dest / child.name)
        else:
            shutil.copy2(child, dest / child.name)


def _readme(scope: dict, eval_result: dict | None, best_round: int | None) -> str:
    name = scope.get("name", scope["id"])
    url = scope.get("url", "—")
    lines = [
        f"# 复刻产物：{name}",
        "",
        f"- 原始网址：{url}",
        f"- 复刻范围：{ '、'.join(f.get('desc','') for f in scope.get('features',[]) if f.get('desc')) }",
    ]
    if best_round is not None:
        lines.append(f"- 最佳精修轮：round{best_round}")
    if eval_result:
        d = eval_result.get("dimensions", {})
        lines += [
            f"- 一致性总分：**{eval_result.get('score','-')}/100**"
            f"（视觉 {d.get('visual','-')} / 功能 {d.get('functional','-')}"
            f" / 交互 {d.get('interaction','-')}）",
        ]
    lines += [
        "",
        "## 目录说明",
        "",
        "- `source/` —— 完整可维护源码（React + TypeScript + Vite 工程）。",
        "- `dist/` —— 已构建的静态产物，零依赖，可独立运行。",
        "",
        "## 独立运行",
        "",
        "方式一（直接看产物，无需 Node）：",
        "```bash",
        "cd dist && python3 -m http.server 8080   # 浏览器打开 http://localhost:8080",
        "```",
        "",
        "方式二（从源码重新构建）：",
        "```bash",
        "cd source && npm install && npm run build  # 产物在 source/dist/",
        "npm run dev                                 # 或本地开发预览",
        "```",
        "",
        "## 说明",
        "",
        "- 搜索结果等动态内容为 **mock 数据**（`source/src/mockData.ts`）：复刻目标是"
        "结果区域的展示与交互逻辑，不代理真实后端，故以本地假数据呈现。",
    ]
    return "\n".join(lines) + "\n"


def package_deliverable(site_id: str) -> Path:
    """把 output/<site> 的当前（=已恢复的最佳轮）源码与 dist 打包到 deliverables/<site>。

    需在 run() 恢复最佳轮并重新构建之后调用，此时 output/<site>/dist 就是最佳产物。
    返回交付目录路径；若缺少 dist 则抛错（说明上游没构建成功）。
    """
    out = ROOT / "output" / site_id
    deliver = ROOT / "deliverables" / site_id
    dist_src = out / "dist"
    if not dist_src.exists():
        raise RuntimeError(f"未找到 {dist_src}，无法打包交付产物（上游可能未成功构建）")

    scope = json.loads((ROOT / "scopes" / f"{site_id}.json").read_text(encoding="utf-8"))
    eval_path = ROOT / "reports" / site_id / "eval.json"
    eval_result = (json.loads(eval_path.read_text(encoding="utf-8"))
                   if eval_path.exists() else None)
    best_round = None
    hist_path = ROOT / "reports" / site_id / "history.json"
    if hist_path.exists():
        best_round = json.loads(hist_path.read_text(encoding="utf-8")).get("best_round")

    if deliver.exists():
        shutil.rmtree(deliver, ignore_errors=True)
    deliver.mkdir(parents=True, exist_ok=True)

    # 1) 干净源码
    _copy_source(out, deliver / "source")
    # 2) 已构建静态产物
    shutil.copytree(dist_src, deliver / "dist")
    # 3) 站点 README
    (deliver / "README.md").write_text(
        _readme(scope, eval_result, best_round), encoding="utf-8")

    print(f"[deliver] 已打包交付产物 → {deliver}")
    return deliver


if __name__ == "__main__":
    import sys

    package_deliverable(sys.argv[1])
