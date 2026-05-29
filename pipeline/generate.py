"""Generate 阶段：把原页截图 + DOM + 功能点交给 Claude，生成 Vite/React 工程。

约定：Claude 以 ===FILE: <相对路径>=== 分隔的多文件格式输出整个工程，
本模块解析后落盘到 output/<site>/（_capture 除外）。

精修闭环时，可附带上一轮的评估反馈（差异点 / 失败断言）让 Claude 修正。
"""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path

from config import DEFAULT_MODEL, get_client

ROOT = Path(__file__).resolve().parent.parent
FILE_RE = re.compile(r"^===FILE:\s*(.+?)\s*===\s*$", re.MULTILINE)


def _img_block(path: Path) -> dict:
    data = base64.standard_b64encode(path.read_bytes()).decode()
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": "image/png", "data": data},
    }


def _build_prompt(scope: dict, capture_meta: dict, feedback: str | None) -> str:
    features = "\n".join(
        f"  - [{f['id']}] ({f.get('type','element')}) {f['desc']}"
        + (f"  原选择器提示: {f['selector_hint']}" if f.get("selector_hint") else "")
        for f in scope["features"]
    )
    desktop = capture_meta["viewports"].get("desktop", {})
    colors = desktop.get("colors", {})
    fonts = desktop.get("fonts", {})

    feedback_section = ""
    if feedback:
        feedback_section = f"""
## 上一轮评估反馈（必须针对性修正）
{feedback}
请重点修复上述低分维度与失败的交互断言。
"""

    return f"""你是资深前端工程师。请复刻目标网页「{scope['name']}」({scope['url']})。
我会提供原页的整页截图、提取的配色/字体信息，以及需要复刻的功能点。

## 复刻范围（只需实现以下功能点，不要多做）
{features}

## 原页视觉信息（供还原参考）
- 主要文字色: {colors.get('text', [])}
- 主要背景色: {colors.get('background', [])}
- 字体族: {fonts.get('family', [])}
- 字号: {fonts.get('size', [])}
{feedback_section}
## 技术要求
1. 用 Vite + React + TypeScript 工程，可 `npm install && npm run build` 构建。
2. 视觉上尽量贴近截图：布局、配色、字体、间距、组件样式。
3. 交互功能点必须真实可用（输入、点击、状态变化、翻页等），数据可用本地 mock。
4. **关键**：为可测试的交互元素加稳定的 `data-testid`，命名用功能点 id（如 data-testid="search-input"）。
   翻页的下一页按钮用 data-testid="next-page"，结果列表用 data-testid="result-list"。
5. 工程自包含，不依赖外部 CDN（字体除外可降级到系统字体）。
6. 不要写任何解释文字，只输出文件。

## 构建必须成功（极重要，否则本轮作废）
- package.json 的 build 脚本只用 `vite build`，**不要**用 `tsc && vite build`（避免类型检查中断构建）。
- tsconfig.json 设 `"noUnusedLocals": false`、`"noUnusedParameters": false`，避免未使用变量导致失败。
- 所有 import 必须真实存在；所有用到的变量/类型都要定义；不要留半成品代码。
- React 18 写法，import 用 `import {{ useState }} from 'react'`。

## 样式必须真正生效（极重要，否则视觉全错）
- 每个 `.css` 文件都必须被某个 `.tsx`/`.ts` 文件 `import`（如 `import './styles.css'`），
  否则 Vite 不会打包它，页面退化成浏览器默认样式（label 与 input 挤同行、按钮变小、布局错乱）。
- 不要生成"孤儿 CSS"：写了样式文件却没人 import。每写一个样式文件，就在对应组件顶部加上它的 import。
- 不要写空的或只有注释的 CSS 文件来占位。

## 输出格式（严格遵守）
对每个文件，先输出一行 `===FILE: 相对路径===`，紧接其完整内容。
必须包含: package.json、vite.config.ts、index.html、src/main.tsx、src/App.tsx 及所需样式/组件。
package.json 的 scripts 至少含 dev/build/preview，依赖只用 react/react-dom + vite + @vitejs/plugin-react + typescript。
现在开始输出工程文件："""


def _parse_files(text: str) -> dict[str, str]:
    """把 ===FILE: path=== 分隔的文本解析成 {相对路径: 内容}。"""
    files: dict[str, str] = {}
    parts = FILE_RE.split(text)
    # parts = [前导, path1, body1, path2, body2, ...]
    for i in range(1, len(parts), 2):
        path = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        body = body.strip("\n")
        # 去掉整体包裹的 ``` 代码围栏（先去前导换行再匹配）
        body = re.sub(r"^```[a-zA-Z0-9]*\n", "", body)
        body = re.sub(r"\n```$", "", body)
        files[path] = body.rstrip() + "\n"
    return files


def generate(scope: dict, feedback: str | None = None, round_no: int = 0) -> Path:
    site_id = scope["id"]
    out = ROOT / "output" / site_id
    capture_meta = json.loads((out / "_capture" / "meta.json").read_text(encoding="utf-8"))

    prompt = _build_prompt(scope, capture_meta, feedback)
    content: list[dict] = [{"type": "text", "text": prompt}]
    # 附原页桌面端截图（视觉参考）
    desktop_png = out / "_capture" / "desktop.png"
    if desktop_png.exists():
        content.append(_img_block(desktop_png))

    client = get_client()
    text = ""
    stop_reason = None
    for attempt in range(3):
        resp = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=16000,
            messages=[{"role": "user", "content": content}],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        stop_reason = resp.stop_reason
        if text.strip() and "===FILE:" in text:
            break
        print(f"[generate] 第{attempt+1}次返回空/无文件(stop={stop_reason})，重试...")

    if stop_reason == "max_tokens":
        print("[generate] 警告：输出可能因 max_tokens 截断，末尾文件或不完整。")

    # 留存 prompt 与响应（满足"体现 AI 使用过程"）
    pdir = ROOT / "prompts" / site_id
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / f"round{round_no}.prompt.md").write_text(prompt, encoding="utf-8")
    (pdir / f"round{round_no}.response.md").write_text(text, encoding="utf-8")

    files = _parse_files(text)
    if not files:
        raise RuntimeError(f"Claude 未按约定格式输出文件，解析为空 (stop={stop_reason})")

    # 清理上一轮源码残留（保留 _capture / node_modules / dist），
    # 避免旧文件干扰本轮构建
    import shutil as _shutil
    _keep = {"_capture", "node_modules", "dist", ".rounds"}
    for child in out.iterdir():
        if child.name in _keep:
            continue
        if child.is_dir():
            _shutil.rmtree(child, ignore_errors=True)
        else:
            child.unlink(missing_ok=True)

    # 落盘，但不碰 _capture 目录
    for rel, body in files.items():
        rel = rel.lstrip("/")
        if rel.startswith("_capture"):
            continue
        fp = out / rel
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(body, encoding="utf-8")

    print(f"[generate] round{round_no} 写入 {len(files)} 个文件 -> {out}")
    _ensure_css_imported(out)
    return out


def _ensure_css_imported(out: Path) -> None:
    """兜底：把没有被任何 .ts/.tsx import 的"孤儿 CSS"自动引入 App/main。

    上游 prompt 已要求每个 .css 都被 import，但模型偶尔漏掉，导致样式不打包、
    页面退化成默认样式。这里做确定性补救：扫描产物，发现孤儿 CSS 就追加 import。
    """
    src = out / "src"
    if not src.exists():
        return
    css_files = [p for p in src.rglob("*.css")]
    if not css_files:
        return
    code_files = list(src.rglob("*.tsx")) + list(src.rglob("*.ts"))
    imported = "\n".join(p.read_text(encoding="utf-8", errors="ignore")
                         for p in code_files)

    # 选锚点：优先 App.tsx，其次 main.tsx
    anchor = src / "App.tsx"
    if not anchor.exists():
        anchor = src / "main.tsx"
    if not anchor.exists():
        return

    orphans = []
    for css in css_files:
        # 任意以该文件名结尾的 import 都算已引用（相对路径不一）
        if f"{css.stem}.css" not in imported:
            orphans.append(css)
    if not orphans:
        return

    import os
    lines = anchor.read_text(encoding="utf-8").splitlines()
    inserts = []
    for css in orphans:
        rel = os.path.relpath(css, anchor.parent).replace(os.sep, "/")
        if not rel.startswith("."):
            rel = "./" + rel
        inserts.append(f"import '{rel}'")
    # 插到最后一个 import 行之后，保持文件头整洁
    last_import = max((i for i, ln in enumerate(lines)
                       if ln.lstrip().startswith("import ")), default=-1)
    lines[last_import + 1:last_import + 1] = inserts
    anchor.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[generate] 兜底：为 {len(orphans)} 个孤儿 CSS 在 {anchor.name} 补 import "
          f"({', '.join(c.name for c in orphans)})")


if __name__ == "__main__":
    import sys

    scope_path = ROOT / "scopes" / f"{sys.argv[1]}.json"
    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    generate(scope)
