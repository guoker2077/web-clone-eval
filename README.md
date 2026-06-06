# 基于 AI 工具的网页复刻与一致性评估

一条**全自动流水线**：给定目标网址与功能范围，自动抓取原页 → 调用 Claude 生成可运行的复刻工程 → 量化评估三维一致性 → 按评估反馈闭环精修，直到达标。

对同类页面，**最小人工输入只有「网址 + 一句自然语言复刻范围」**——系统自动探测页面 DOM、合成结构化 `scope.json`，无需手写选择器或测试脚本，也无需改代码、人工干预 AI。（仍保留手写 `scope.json` 作为精确控制的备选。）

## 核心特性

- **零脚本输入**：`synthesize_scope.py` 把「URL + 自然语言范围」自动展开成可驱动复刻与评估的结构化 scope，selector 取自真实 DOM，并经确定性校验。
- **稳定复用**：新页面只给一句范围描述，流水线自动完成复刻与评估。
- **闭环精修（看图对比）**：评估后把「原页 + 上一轮复刻页」两张截图一起回灌，配合 LLM 逐模块诊断，让模型对比着改而非盲修；分数驱动质量提升。
- **agent 记忆（跨站学习 · RAG）**：诊断 agent 在每个 run 结束后复盘所有信号，提炼「模块类型级」教训存入全局记忆库，下次生成前用**向量语义检索**召回相关教训注入「避坑清单」（跨类型、跨语言）——一处踩坑、处处规避。
- **截断自愈**：生成被 `max_tokens` 截断时用 prefill 续写无缝补全，杜绝半截工程落盘。
- **可量化可置信**：SSIM、CIEDE2000、pHash、IoU、断言通过率等业界指标，逐模块裁剪比对；确定性指标可复现，并与 LLM 视觉分交叉验证（一致/存疑）。
- **全自动评估 + 可独立运行交付**：复刻后构建→截图→打分→出报告→打包 `deliverables/<site>` 一键完成，产物零依赖可独立运行。
- **并发异步服务**：云端 worker 单进程内多并发循环（`WORKER_CONCURRENCY`），受内存约束横向扩；SQLite 原子认领保证不重复领单。

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
② Generate   Claude(claude-opus-4-8, 视觉输入) ← 截图 + 功能点 + 历史避坑清单(记忆)
             → 生成 Vite/React/TS 工程（截断则 prefill 续写补全）
   ▼
   Build      npm install && npm run build → 起静态服务
   ▼
③ Evaluate   原页 vs 复刻页 → 视觉(逐模块裁剪 SSIM/像素/pHash) + 功能(覆盖率/断言)
             + 交互(状态/流程) + LLM 交叉验证（可置信）
   ▼
④ Refine     分数 < 阈值 → 「原页+复刻页」双图 + 逐模块诊断回灌 Claude → 回到② (限 N 轮)
   │
   ▼ 达标
  报告 (report.md + eval.json + 截图) → 打包交付 deliverables/<site>
   │
   ▼ run 结束
⑤ Learn      诊断 agent 复盘全轮信号 → 提炼模块类型级教训 → 写入记忆库(候选→生效→退役)
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
│  ├─ diagnose.py         #   ⑤ 诊断 agent：复盘信号、提炼跨站教训
│  ├─ diagnose_match.py   #   scope → 规范化模块类型（教训注入的相关性键）
│  ├─ pitfall_memory.py   #   agent 记忆库：教训存储/生命周期/按需注入
│  ├─ report.py           # 渲染 Markdown 报告
│  ├─ deliver.py          # 打包可独立运行的交付产物 deliverables/<site>
│  ├─ run.py              # ④ 总控闭环（含看图对比反馈 + run 末学习）
│  └─ check_api.py        # API 连通性自测
├─ server/                # 云端异步服务（提交→后台跑→轮询→预览）
│  ├─ app.py              #   FastAPI：提交/查询/进度 API + 预览路由 + UI（含鉴权）
│  ├─ worker.py           #   worker：多并发认领队列任务，子进程/docker 沙箱跑 runner
│  ├─ runner.py           #   单 job 执行体（合成+闭环），进度回写 + setrlimit
│  ├─ jobstore.py         #   SQLite 任务库+队列（WAL+原子认领）+ 配额计数
│  ├─ quota.py            #   提交闸门：IP 限流/在途上限/每日总量
│  └─ static/             #   最小交互界面（表单+轮询+一键跳转）
├─ tests/unit/            # 一键单测（离线/确定/秒级，docker compose run --rm test）
├─ scopes/                # 每个站点一份 scope.json（唯一人工输入）
├─ output/<site>/         # 复刻产物（独立可运行的 Vite 工程）
│  └─ _capture/           #   原页抓取的截图/DOM/meta
├─ deliverables/<site>/   # 交付产物：source/（可维护源码）+ dist/（独立运行）+ README
├─ memory/                # agent 记忆库 pitfalls.json（跨站教训，可清空，见下）
├─ reports/<site>/        # 评估报告 + 复刻页截图 + 历史
├─ prompts/<site>/        # 留存的 prompt 与 Claude 响应（体现 AI 使用过程）
├─ run_logs/              # 运行日志 + EVIDENCE.md（可复现性与量化数据分析证据）
├─ requirements.txt
├─ Dockerfile             # 一体化运行镜像（Playwright+Node+中文字体，非 root）
├─ docker-entrypoint.sh   # 入口：修正卷属主后降权到非 root 运行
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

> **加固状态**：骨架已补齐对外开放所需的三项加固——
> ① SSRF 防御、② 进程隔离 + 非 root 容器、③ 限流/配额/最小鉴权（见下）。
> 仍为**单机形态**：单 worker、SQLite 当队列、子进程（或可选 docker）当沙箱；
> 上云只需「换组件不改逻辑」（见「上云部署」）。

### SSRF 防御（拦内网 / 云元数据 / 重定向）

云端要替**陌生人**用无头浏览器抓**任意 URL**——这是教科书级的 SSRF 风险：攻击者可提交
`http://169.254.169.254/...`（偷云厂商 IAM 凭证）、`http://127.0.0.1:6379`（打内网 Redis）、
`http://10.x / 192.168.x`（打内网主机）、`file:///etc/passwd`（越权读本地）。
`pipeline/ssrf_guard.py` 提供纵深防御，**三个接入点**：

1. **提交时**（`app.py`）——主闸门 `assert_url_allowed(url)`：scheme 白名单（仅 http/https）、
   端口白名单（挡 6379/3306/22 等内网服务端口）、host 解析后逐 IP 判网段（拦
   链路本地/私有/环回/保留段），明显非法直接 400。
2. **抓取前**（`capture` / `probe_dom`）——`protect_context` 再解析一次 DNS 并复检，
   并把已解析 IP 回传，**防 DNS rebinding**（提交与抓取之间域名重解析成内网）。
3. **导航中**（Playwright route）——`guard_route` 拦截页面每一跳请求，**防 30x 重定向
   到内网**或页面内请求内网资源；按 (scheme,host,port) 缓存判定，避免逐子资源重复解析。

```bash
# 开关：仅当 SSRF_GUARD 为真时启用。
# 云端 web/worker 默认开（compose 已设 SSRF_GUARD=1）；
# 本地 CLI（pipeline 服务）默认关，方便复刻 http://localhost:3000 等自有开发页。
```

> 与网络层（worker 私有子网 + 出口过滤）配合构成纵深防御：即便应用层被绕过，
> 网络层仍兜底拦截。

### 进程隔离 + 非 root 容器（限资源、缩影响面）

抓取陌生人页面的进程不该是 root，也不该能拖垮整机。两层：

1. **非 root 运行**：镜像建 `app`（UID 1000）用户；容器以 root 起、入口脚本
   （`docker-entrypoint.sh`）先把挂载卷属主 `chown` 给 app、再 `setpriv` 降权执行。
   这同时**根治了产物被 root 占有、宿主机普通用户删不掉**的问题。
2. **资源上限**：`runner` 跑 job 前用 `setrlimit` 限 CPU 时间 / 单文件大小 / 进程数
   （**反 fork 炸弹**），子进程（npm/chromium）自动继承。开关 `JOB_RLIMIT`，
   阈值见 `JOB_CPU_SEC / JOB_FSIZE_MB / JOB_NPROC`。
   > 刻意不设地址空间上限（`RLIMIT_AS`）——Chromium 映射巨量虚拟内存，会被它搞崩；
   > 内存上限交给容器层（下方 docker 沙箱的 `--memory`，或云任务规格）。

可选**强隔离**：把 worker 的 `SANDBOX_MODE` 设为 `docker`，则每个 job 关进一次性
容器（`docker run --rm --memory --cpus --pids-limit --cap-drop=ALL
--security-opt no-new-privileges`）。代价是 worker 需能调宿主 docker（挂
`/var/run/docker.sock`，本身是提权面）——单机演示够用，生产建议换 rootless docker
或直接用云任务 API（见「上云部署」）。默认 `subprocess`（同容器 + setrlimit 软隔离）。

### 限流 / 配额 / 最小鉴权（防滥用与成本失控）

每个 job 都是真金白银的 Claude 调用，对外开放后必须设闸：

- **最小鉴权（HTTP Basic）**：设了 `BASIC_AUTH_USER/PASS` 就开、留空就关。
  **公开到公网前必设**，否则任何人都能刷你的额度。本地调试可留空、零摩擦。
- **三道配额闸**（`QUOTA_GUARD=1` 开启，`server/quota.py`）：
  ① 按 IP 限流（`QUOTA_IP_MAX` / `QUOTA_IP_WINDOW_SEC`，挡单点刷量）；
  ② 全局在途上限（`QUOTA_ACTIVE_MAX`，队列背压）；
  ③ 每日总量上限（`QUOTA_DAILY_MAX`，成本总闸）。超限返回 `429` + 可读消息。

计数现落 SQLite，上云原样换 Redis 的原子 `INCR`+TTL，逻辑不变。
另强烈建议在 Claude 平台侧设**账单告警/预算上限**作为最后一道兜底。

### 服务端环境变量一览

| 变量 | 默认 | 作用 | 谁用 |
| --- | --- | --- | --- |
| `SSRF_GUARD` | 关 | 开启 SSRF 防御 | web/worker |
| `BASIC_AUTH_USER/PASS` | 空 | Basic 鉴权账号密码（留空=关） | web |
| `QUOTA_GUARD` | 关 | 开启配额闸门 | web |
| `QUOTA_IP_MAX` / `QUOTA_IP_WINDOW_SEC` | 5 / 3600 | 单 IP 每窗口任务上限 | web |
| `QUOTA_ACTIVE_MAX` | 20 | 全局在途上限 | web |
| `QUOTA_DAILY_MAX` | 200 | 全站每日总量 | web |
| `JOB_RLIMIT` | 关 | 给 job 套 setrlimit | worker |
| `JOB_CPU_SEC` / `JOB_FSIZE_MB` / `JOB_NPROC` | 900 / 512 / 512 | 各项资源上限 | worker |
| `JOB_TIMEOUT_SEC` | 1800 | 单 job 墙钟上限 | worker |
| `WORKER_CONCURRENCY` | 2 | 单 worker 进程内并行 job 数（受内存约束：16G 建议 4~6，2核4G 建议 2，应 ≤ `QUOTA_ACTIVE_MAX`） | worker |
| `SANDBOX_MODE` | subprocess | `docker`=每 job 一次性容器 | worker |

> `docker compose up web worker` 已在 compose 里把 SSRF/配额/rlimit 默认打开；
> 只需在 `.env` 补 `BASIC_AUTH_USER/PASS` 即可公开。

### 上云部署（单机 CVM 起步 → 托管件按需替换）

整套已 Docker 化，**最小上云路径＝一台云服务器 + docker compose**：

```bash
# 在云服务器上（建议 ≥4GB 内存，Playwright+npm 构建吃内存）
git clone <repo> && cd web-clone-eval
cp .env.example .env       # 填 Claude token + BASIC_AUTH_USER/PASS
docker compose build
docker compose up -d web worker
# 前置 nginx 反代 + 域名 + TLS（Let's Encrypt），把 80/443 转到 web 的 8000
```

> nginx 记得透传 `X-Forwarded-For`，配额限流才能拿到真实客户端 IP。

要减运维时，按下表「换组件不改逻辑」逐步托管化（如腾讯云：web 上**云托管**容器
PaaS、产物丢 **COS + CDN**、队列换托管 **Redis**；worker 因是重算力后台任务，
更适合常驻容器/云任务而非函数）：

| 单机现状 | 托管替换 | 收益 |
| --- | --- | --- |
| 子进程 / docker 沙箱 | 云任务（Cloud Run Job / Fargate / k8s Job） | 原生资源&网络隔离，无需挂 docker.sock |
| SQLite 队列+计数 | Redis（队列+限流）+ Postgres（状态） | 多实例并发、横向扩 worker |
| 产物卷挂载 | 对象存储（COS/S3）+ CDN + 独立域名 | 预览各占 origin，省掉 asset 路径重写 |
| `.env` 注入 | Secret Manager | 密钥不落盘 |
| 应用层 SSRF | + worker 私有子网 + 出口过滤 | 纵深防御 |



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

## 一键测试

核心逻辑单测——**离线、确定、秒级、零成本**（不联网、不调 Claude API、不需要 token），
覆盖可置信指标的可复现性、交叉验证判定、功能覆盖率、范围对齐 rubric、SSRF 防御、
以及队列的并发认领原子性（背书并发执行的正确性）：

```bash
docker compose run --rm test          # 一键跑全部单测（推荐）
# 或本地：pip install -r requirements.txt && pytest
```

> 设计分层：把「调模型/联网」的慢且不确定的部分隔离在单测之外（用 `check_api.py`
> 与提交一个真实 job 做手动冒烟），单测只覆盖纯逻辑，故可放进 CI 反复跑。
> 测试代码见 `tests/unit/`，约 68 个用例 1~2 秒跑完。

## agent 记忆（跨站学习 + 可清空）

每个 run 结束后，**诊断 agent**（`pipeline/diagnose.py`）复盘整轮的所有信号——客观的
（build 报错、孤儿 CSS、失败的交互断言）与解释性的（LLM 逐模块诊断）——把**复发性、
结构性**的问题提炼成一条**跨站可复用、模块类型级**的教训，存入全局记忆库
`memory/pitfalls.json`。下次**任何同类型模块**的页面在生成前，按相关性把相关教训注入
prompt 当「避坑清单」——一处踩坑、处处规避。

防污染靠教训的生命周期 + 信用分配：

```
candidate（候选，确认 <2 次，不注入）
  → active（生效，独立确认 ≥2 次，注入 prompt）
  → retired（退役，注入后连续无效则停止注入）
```

- 「独立确认 ≥2 次」按**不同 run** 计数；但**客观信号**（build 报错等）若在**同一个
  run 内跨多轮反复**出现，就地折算满足 ≥2（编译器铁证不浪费一轮）；解释性信号不享此豁免。
- 信用分配只看**该模块类型**的分数变化（而非总分），把全局归因缩成单模块归因。
- **语义召回（RAG）**：注入时不靠关键词精确分桶，而是把当前页的「页面名+功能点描述」
  embed 成向量，在所有 active 教训里按余弦相似度召回 top-k。用多语言模型
  （paraphrase-multilingual-MiniLM-L12-v2, 384 维, 本地 ONNX）——**跨类型 + 跨语言**：
  「搜索提交按钮」能召回挂在「登录提交按钮」下的 loading 教训，中文教训也能被
  英文 scope 描述召回（实测 中↔英 相似度 0.58 > 无关项 0.34）。embedder 不可用时
  优雅降级到关键词精确匹配——RAG 是增强，不是单点依赖。
- 全局存、**按相关性取**：只注入语义相关的 top-k active 教训，避免 context 膨胀与污染放大。

> embedding 模型经 modelscope（国内可靠）在镜像构建期预下载，运行时零网络等待。
> 升级到语义召回后，旧教训可用 `pitfall_memory.backfill_embeddings()` 一次性补算向量。

**清空记忆（部署时按需）**：记忆库是纯数据文件，删掉即从零开始积累：

```bash
rm -f memory/pitfalls.json     # 清空所有已学教训，下次 run 重新积累
```

> 仓库里**预置了**我们真实跑出来的教训（体现「项目确实在学习」）。自行部署时若想要
> 干净起点，按上面命令清空即可——不影响任何功能，只是重新开始学。
> 记忆库以卷挂载（`./memory`）持久化，容器删除后教训仍在本地。

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
因此合成产物可直接驱动复刻与评估（实测 GitHub 登录页：云端 API 自动合成版闭环
得分 92.8，与手写 scope 的 CLI 版 95.1 基本持平，证明自动化链路可独立复现结果）。

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

> **范围对齐评分**：视觉指标按 scope 声明的模块**逐块裁剪比对**（原页 bbox 来自
> capture，复刻页来自 `data-testid`），不拿整页比——避免复刻页因缺少范围外内容
> （壁纸/资讯流/页脚）被冤枉扣分（生成目标≠评估目标）。整页指标仅作参考留档。
> LLM 辅助评分同样只评声明模块。

> **可置信设计**：① 确定性指标（SSIM 等）同输入必得同输出、bit-for-bit 可复现，
> 与非确定的 LLM 分明确分离；② 所有比率附原始计数（如断言 5/5）；③ **交叉验证**
> ——确定性视觉分与 LLM 视觉分两种独立方法相互印证，差距≤15 判「一致」、否则
> 「存疑」提示复核。报告中并列展示（详见 [EVIDENCE.md](run_logs/EVIDENCE.md)）。

> **LLM 辅助评分（加分项）**：除上述确定性指标外，额外让 Claude 视觉模型同时看原页与复刻页，按 rubric 打分（`metrics_llm.py`）。因 LLM 评分非确定性，**不计入主总分**，仅作辅助信号与确定性指标交叉验证，在报告中并列展示。实测它对纯视觉还原度更敏感，能补充 SSIM 之外的人眼直觉判断。

## 复刻结果

4 个不同类型页面（1 内容展示型 + 3 表单交互型：登录×1、搜索×2），均跑完闭环精修。
完整可引用的证据与数据分析见 [run_logs/EVIDENCE.md](run_logs/EVIDENCE.md)。

| 序号 | 类型 | 原始网址 | 复刻需求 | 交付产物 | 综合得分 | 视觉/功能/交互 | LLM辅助 | 交叉验证 | 报告 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 登录表单 | https://github.com/login | 用户名/密码/登录交互/必填校验 | [deliverables/github-login](deliverables/github-login) | **95.1** | 92.7 / 100 / 90.0 | 95 | 差2.3 ✅一致 | [report](reports/github-login/report.md) |
| 2 | 内容展示 | MDN `<a>` 文档页 | 导航/面包屑/正文/代码块/右侧大纲 | [deliverables/mdn-doc](deliverables/mdn-doc) | **80.2** | 50.6 / 100 / 100 | 84 | 差33.4 ⚠️存疑 | [report](reports/mdn-doc/report.md) |
| 3 | 搜索表单 | https://www.baidu.com | 搜索框/按钮/结果列表/翻页 | [deliverables/baidu](deliverables/baidu) | **79.2** | 79.6 / 83.3 / 70.0 | 82 | 差0.1 ✅一致 | [report](reports/baidu/report.md) |
| 4 | 搜索表单 | https://www.bing.com | 搜索框/按钮/结果列表/翻页 | [deliverables/bing](deliverables/bing) | **67.5** | 58.6 / 75.0 / 70.0 | 79 | 差20.4 ⚠️存疑 | [report](reports/bing/report.md) |

每站交付物含三部分：`source/`（可长期维护的 React+TS+Vite 源码）、`dist/`（已构建、
零依赖、可独立运行的静态产物）、`README.md`（运行说明 + 评分摘要 + mock 数据声明）。

```bash
# 直接运行交付产物（无需 Node，任意静态服务器）
cd deliverables/<site>/dist && python3 -m http.server 8080   # 浏览器开 http://localhost:8080
# 或从源码重建
cd deliverables/<site>/source && npm install && npm run dev
```

> **关于「交叉验证」列**：确定性视觉分（SSIM 等，可复现）与 LLM 视觉分（独立视角）
> 的差距。二者接近（≤15）判「一致」，是评分可信的强证据；差距大判「存疑」，提示
> 人工复核。GitHub/百度两法差距仅 2.3/0.1，必应/MDN 标存疑也属正确——指标能如实
> 暴露分歧而非一律打高分，正是「可置信」的体现（详见 EVIDENCE.md §3.2）。

## 关于 AI 工具使用

本项目复刻产物由 **Claude (`claude-opus-4-8`)** 通过 API 生成。每一轮的 prompt 与模型响应完整保存在 `prompts/<site>/round*.{prompt,response}.md`，提交记录中可追溯 AI 的生成与精修过程。

