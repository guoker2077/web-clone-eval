# 基于 AI 工具的网页复刻与一致性评估

一条**全自动流水线**：给定目标网址与功能范围，自动抓取原页 → 调用 Claude 生成可运行的复刻工程 → 量化评估三维一致性 → 按评估反馈闭环精修，直到达标。

对同类页面，**最小人工输入只有「网址 + 一句自然语言复刻范围」**——系统自动探测页面 DOM、合成结构化 `scope.json`，无需手写选择器或测试脚本，也无需改代码、人工干预 AI。（仍保留手写 `scope.json` 作为精确控制的备选。）

## 核心特性

- **零脚本输入**：`synthesize_scope.py` 把「URL + 自然语言范围」自动展开成可驱动复刻与评估的结构化 scope，selector 取自真实 DOM，并经确定性校验。
- **稳定复用**：新页面只给一句范围描述，流水线自动完成复刻与评估。
- **闭环精修**：评估分数（视觉差异、失败的交互断言）回灌给 Claude 重新生成，分数驱动质量提升。
- **可量化可置信**：采用 SSIM、CIEDE2000、pHash、IoU、断言通过率等业界公认指标，多视口测量，加权合成总分，权重透明可调。
- **全自动评估**：复刻后无需人工驱动，构建→截图→打分→出报告一键完成。

## 流水线架构

```
网址 + 自然语言复刻范围  (最小人工输入)
   │
   ▼
⓪ Synthesize 轻量探测 DOM → Claude 合成 → 确定性校验 → scope.json
   │                                    （也可跳过，直接手写 scope.json）
   ▼
① Capture    Playwright 抓原页 → 多视口整页截图 + DOM 快照 + 配色/字体 + 关键元素 bbox
   ▼
② Generate   Claude(claude-opus-4-8, 视觉输入) ← 截图+功能点 → 生成 Vite/React/TS 工程
   ▼
   Build      npm install && npm run build → 起静态服务
   ▼
③ Evaluate   原页 vs 复刻页 → 视觉(SSIM/像素/pHash) + 功能(覆盖率/断言) + 交互(状态/流程)
   ▼
④ Refine     分数 < 阈值 → 差异点+失败断言回灌 Claude → 回到② (限 N 轮，全自动)
   │
   ▼ 达标
  报告 (report.md + eval.json + 截图)
```

## 目录结构

```
web-clone-eval/
├─ pipeline/              # 流水线代码
│  ├─ config.py           # Claude 客户端（兼容中转 token / 官方 key）
│  ├─ synthesize_scope.py # ⓪ 合成 scope（URL+自然语言 → 结构化 scope.json）
│  ├─ capture.py          # ① 抓取
│  ├─ generate.py         # ② 生成
│  ├─ evaluate.py         # ③ 评估（构建+截图+打分）
│  ├─ metrics_visual.py   #   视觉度量 SSIM/像素/pHash/CIEDE2000/IoU
│  ├─ metrics_behavior.py #   功能&交互度量（Playwright 跑断言）
│  ├─ metrics_llm.py      #   LLM 辅助视觉评分（加分项，交叉验证）
│  ├─ report.py           # 渲染 Markdown 报告
│  ├─ run.py              # ④ 总控闭环
│  └─ check_api.py        # API 连通性自测
├─ server/                # 云端异步服务（提交→后台跑→轮询→预览）
│  ├─ app.py              #   FastAPI：提交/查询/进度 API + 预览路由 + UI
│  ├─ worker.py           #   worker：认领队列任务，子进程跑 runner
│  ├─ runner.py           #   单 job 执行体（合成+闭环），进度回写
│  ├─ jobstore.py         #   SQLite 任务库+队列（WAL+原子认领）
│  └─ static/             #   最小交互界面（表单+轮询+一键跳转）
├─ scopes/                # 每个站点一份 scope.json（唯一人工输入）
├─ output/<site>/         # 复刻产物（独立可运行的 Vite 工程）
│  └─ _capture/           #   原页抓取的截图/DOM/meta
├─ reports/<site>/        # 评估报告 + 复刻页截图 + 历史
├─ prompts/<site>/        # 留存的 prompt 与 Claude 响应（体现 AI 使用过程）
├─ requirements.txt
├─ Dockerfile             # 一体化运行镜像（Playwright+Node+中文字体）
├─ docker-compose.yml     # 构建/运行编排（卷挂载产物、env_file 注入密钥）
├─ .dockerignore
├─ .env.example
└─ .gitignore
```

## 环境要求

两种方式择一：

- **Docker（推荐）**：只需 Docker（含 Compose）。环境全部打包，见下方「Docker 运行」。
- **本地安装**：Python 3.10+（建议 venv）、Node.js 18+ 与 npm（构建复刻产物）、Claude API（官方 key 或兼容中转平台）。

## 快速开始

```bash
# 1. Python 依赖
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Playwright 浏览器内核（国内用镜像）
PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright \
  playwright install chromium

# 3. 配置 API（复制后填入真实值）
cp .env.example .env

# 4. 验证 API 连通
cd pipeline && python check_api.py

# 5. 跑完整闭环（以百度为例）
python run.py baidu --max-rounds 3 --threshold 85
```

## Docker 运行（推荐，免装环境）

把 Python 流水线、Node 构建链、版本匹配的 Playwright Chromium、中文字体一次性打包，
避免本地踩浏览器内核下载与 CJK 字体「方框」的坑，也为云端托管提供可迁移的运行单元。

```bash
# 1. 配置密钥（.env 不会被打进镜像，运行时由 env_file 注入）
cp .env.example .env   # 填入真实 token

# 2. 构建镜像
docker compose build

# 3. 合成 scope（URL + 自然语言范围）
docker compose run --rm pipeline \
  python synthesize_scope.py https://github.com/login "复刻用户名/密码/登录按钮，验证登录与必填校验"

# 4. 跑完整闭环（产物经卷挂载落回宿主机 output/ reports/ prompts/）
docker compose run --rm pipeline python run.py github-login --max-rounds 2

# 5. 预览复刻产物（暴露 8080 端口，浏览器访问 http://localhost:8080）
docker compose run --rm --service-ports pipeline \
  python -m http.server 8080 --directory /app/output/github-login/dist
```

> 镜像基于 Docker Hub 的 `python:3.11-slim`，构建期自行安装 Node.js、Playwright
> Chromium（走 npmmirror 镜像）与中文字体——不依赖国内难拉的 `mcr.microsoft.com`，
> 任何能访问 Docker Hub 的环境都能构建。`evaluate` 阶段构建复刻产物需要 npm/npx，
> 已一并装入。产物目录与 `scopes/` 以卷挂载，容器删除后结果仍在本地。

## 云端异步服务（Web UI：提交 → 后台跑 → 一键预览）

除 CLI 外，本项目提供一套**异步任务服务**：用户在网页上只填「网址 + 自然语言范围」，
提交后立即拿到任务、后台自动跑完整闭环（合成 scope → 复刻 → 评估 → 精修），
页面实时显示进度，完成后一键跳转预览复刻页与评估报告。这是云端托管的可运行雏形。

```bash
# 起 API + worker（共享 ./data 下的队列 DB）
docker compose up web worker
# 浏览器打开 http://localhost:8000 ，填网址+复刻范围，提交即可
```

也可本地直接跑（不经 Docker）：

```bash
cd web-clone-eval
# 终端 1：API + UI
JOBS_DB="$PWD/server/jobs.db" .venv/bin/python -m uvicorn server.app:app --port 8000
# 终端 2：worker（认领队列任务）
JOBS_DB="$PWD/server/jobs.db" .venv/bin/python -m server.worker
```

架构（提交与执行解耦，为云端弹性伸缩铺路）：

```
浏览器 UI ──POST /api/jobs──▶ FastAPI(web, 无状态)
                                  │ 入队
                                  ▼
                          SQLite 队列(./data/jobs.db)   ← 上云换 Redis+Postgres
                                  │ 原子认领
                                  ▼
                          worker ──子进程──▶ runner(合成+闭环)
                                  │ 进度/分数回写            ↑ 上云换 docker run 沙箱
                                  ▼
                       web 轮询 /api/jobs/{id}/logs → UI 实时进度
                       完成后 /preview/{site} 预览、/report/{site} 看报告
```

关键接口：`POST /api/jobs`（提交）、`GET /api/jobs/{id}`（状态/分数）、
`GET /api/jobs/{id}/logs?after_id=N`（增量进度）、`GET /preview/{site}/`（预览产物）。

> 当前为**本地骨架**：单 worker 串行、SQLite 当队列、子进程当沙箱、仅校验 URL scheme。
> 对外开放前需补三项加固：SSRF 防御（拦内网/元数据 IP、重定向重验）、
> 每 job 沙箱容器（资源/网络限制）、限流与配额（防滥用与成本失控）。
> worker 调 runner 的子进程边界即为未来 `docker run` 沙箱的接入点。

`.env` 支持两种鉴权方式（择一）：

| 场景 | 变量 |
| --- | --- |
| 官方 API | `ANTHROPIC_API_KEY` |
| 中转平台 | `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL` |

> 注意：中转平台只能用 `AUTH_TOKEN`，**不要**同时设置 `API_KEY`——SDK 会同时发送 `X-Api-Key` 头导致网关 401。`.env` 已被 `.gitignore` 排除，切勿提交。

## 命令

```bash
python synthesize_scope.py <url> "<自然语言复刻范围>"  # ⓪ 合成 scope.json（可选 --id）
python run.py <site>                  # 完整闭环：capture→generate→build→eval→refine
python run.py <site> --skip-capture   # 复用已抓取的原页
python run.py <site> --max-rounds 3   # 最大精修轮数
python run.py <site> --threshold 85   # 达标阈值（0-100）

python capture.py <site>              # 单独跑抓取
python generate.py <site>             # 单独跑生成
python evaluate.py <site>             # 单独跑构建+评估
python report.py <site>               # 渲染报告
```

## 新增一个复刻页面

### 方式 A：自动合成 scope（推荐，最小输入）

只给网址和一句自然语言范围，系统自动探测 DOM 并合成 `scopes/<id>.json`：

```bash
cd pipeline
python synthesize_scope.py https://github.com/login \
  "复刻用户名/密码输入框、Sign in 登录按钮、注册链接，验证登录交互与必填校验"
# → 生成 scopes/github-login.json，随后即可 python run.py github-login
```

合成过程：① Playwright 轻量抓取目标页的真实交互元素清单（tag/id/name/选择器）；
② Claude 把自然语言范围 + 真实元素清单展开成结构化 features；
③ **确定性校验**——强制 `action` 落在白名单、behavior 的 `target` 必须引用已声明的 element、
element 必须有真实 `selector_hint`，校验不过会回灌让模型自修。
因此合成产物可直接驱动复刻与评估（实测 GitHub 登录页合成版闭环得分 94.3，与手写版持平）。

> 站点 `id` 默认从 URL 推断（可用 `--id` 指定）。selector 取自**原页 DOM**，
> 对结构复杂或重度动态渲染的页面合成质量会下降，此时建议改用方式 B 手写精确控制。

### 方式 B：手写 scope（精确控制）

直接在 `scopes/` 下新建 `<site>.json`，无需改任何代码：

```jsonc
{
  "id": "github-login",
  "name": "GitHub 登录页",
  "url": "https://github.com/login",
  "type": "form",
  "viewports": [{ "name": "desktop", "width": 1280, "height": 800 }],
  "wait": { "until": "networkidle", "extra_ms": 1000 },
  "features": [
    { "id": "username", "type": "element", "desc": "用户名输入框",
      "selector_hint": "#login_field" },
    { "id": "login-submit", "type": "behavior", "desc": "填表后点击登录",
      "steps": [
        { "action": "fill", "target": "username", "value": "demo" },
        { "action": "click", "target": "submit-button" }
      ]}
  ],
  "masks": [{ "desc": "动态验证码", "selector": ".captcha" }]
}
```

字段说明：
- `features[].type`: `element`（检查存在/可见）或 `behavior`（执行 steps 断言）
- `steps[].action`: `fill` / `click` / `expect_visible` / `expect_text`
- `steps[].target`: **必须是某个已声明 element feature 的 id**（不是 CSS 选择器）
- 复刻页约定为可测试元素加 `data-testid="<feature-id>"`，评估据此定位
- `masks`: 动态区域（广告/验证码）在视觉对比前遮罩，避免污染分数

## 评估指标

| 维度 | 权重 | 指标 | 说明 |
| --- | --- | --- | --- |
| 视觉 | 0.4 | SSIM / MS-SSIM | 结构相似度，0-1 越高越好 |
| | | 像素差异率 | 超阈值像素占比，越低越好 |
| | | pHash 汉明距离 | 感知哈希，0-64 越低越相似 |
| | | CIEDE2000 ΔE | 主色板色差（色彩还原度） |
| | | bbox IoU | 关键元素布局重合度 |
| 功能 | 0.4 | 元素存在率 | scope 功能点对应元素是否齐备 |
| | | 行为通过率 | 交互流程是否整体跑通 |
| 交互 | 0.2 | 断言通过率 | 逐操作断言 pass/fail |
| | | 状态反馈 | 输入控件 focus 等状态样式变化 |
| _加分项_ | — | LLM 辅助视觉评分 | Claude 视觉模型按 rubric 交叉验证（布局/配色/排版/组件），非确定性，不计入主总分 |

**总分** = 视觉×0.4 + 功能×0.4 + 交互×0.2（满分 100）。权重定义在 `evaluate.py` 的 `WEIGHTS`，透明可调。所有截图统一缩放后比较，多视口取均值。

> **LLM 辅助评分（加分项）**：除上述确定性指标外，额外让 Claude 视觉模型同时看原页与复刻页，按 rubric 打分（`metrics_llm.py`）。因 LLM 评分非确定性，**不计入主总分**，仅作辅助信号与确定性指标交叉验证，在报告中并列展示。实测它对纯视觉还原度更敏感，能补充 SSIM 之外的人眼直觉判断。

## 复刻结果

3 类页面（1 内容展示型 + 2 表单交互型），均跑完闭环精修，分数见各报告：

| 序号 | 类型 | 原始网址 | 复刻需求 | 前端代码 | 综合得分 | 视觉/功能/交互 | LLM辅助 | 报告 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 内容展示 | https://www.baidu.com | 搜索框/按钮/结果列表/翻页 | [output/baidu](output/baidu) | **77.5** | 75.3 / 83.3 / 70.0 | 桌面84 / 移动70 | [report](reports/baidu/report.md) |
| 2 | 表单交互 | 微信支付登录页 | 用户名/密码/验证码/登录 | [output/wxpay-login](output/wxpay-login) | **77.9** | 44.7 / 100 / 100 | 桌面62 | [report](reports/wxpay-login/report.md) |
| 3 | 表单交互 | https://github.com/login | 用户名/密码/登录交互/必填校验 | [output/github-login](output/github-login) | **93.6** | 88.9 / 100 / 90.0 | 桌面92 | [report](reports/github-login/report.md) |

> 启动任一复刻产物：`cd output/<site> && npm install && npm run dev`。

## 关于 AI 工具使用

本项目复刻产物由 **Claude (`claude-opus-4-8`)** 通过 API 生成。每一轮的 prompt 与模型响应完整保存在 `prompts/<site>/round*.{prompt,response}.md`，提交记录中可追溯 AI 的生成与精修过程。

