# 基于 AI 工具的网页复刻与一致性评估 —— 一体化运行镜像
#
# 基础镜像选型说明：
#   官方 Playwright 镜像（mcr.microsoft.com/...）在国内网络下基本拉不动，
#   故改用 Docker Hub 的 python:3.11-slim（可秒拉），在构建期自行安装：
#     - Node.js（evaluate 阶段构建 Vite/React 复刻产物需 npm/npx）
#     - Playwright Chromium（走 npmmirror 镜像，规避官方 CDN 卡顿）
#     - 中文字体（修复复刻截图「方框」问题，视觉评估前提）
#   这样彻底摆脱对 MCR 的依赖，迁移性最好（任何能访问 Docker Hub 的环境都能构建）。
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    NPM_CONFIG_REGISTRY=https://registry.npmmirror.com \
    # Playwright 浏览器内核走淘宝镜像
    PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright \
    # 浏览器装到共享路径（非 root 用户也能读），而非 root 家目录
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers

# 1) 系统依赖 + Node.js + 中文字体
#    - curl/gnupg：装 NodeSource
#    - fonts-noto-cjk：CJK 字体，修复截图方框
#    - util-linux：提供 setpriv，入口脚本降权用
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl gnupg ca-certificates fontconfig fonts-noto-cjk util-linux \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && fc-cache -f \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Python 依赖（先拷 requirements，利用层缓存）
COPY requirements.txt ./
RUN pip install -r requirements.txt

# 3) Playwright Chromium 及其运行所需系统库
#    playwright install --with-deps chromium 会自动补齐 Chromium 的系统依赖。
#    装到 /opt/pw-browsers（见上 ENV），并放开读权限，非 root 用户也能启动浏览器。
RUN playwright install --with-deps chromium \
    && chmod -R a+rX /opt/pw-browsers

# 3.5) 预下载语义检索 embedding 模型（教训 RAG 用）。经 modelscope（国内可靠）拉
#      多语言小模型到共享缓存，避免运行时赌 HuggingFace 网络；非 root 也能读。
#      下载失败不让构建中断——运行时 embedder 不可用会自动降级到关键词匹配。
ENV FASTEMBED_CACHE_PATH=/opt/fastembed-cache \
    EMBED_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
RUN python3 -c "from modelscope import snapshot_download; \
    snapshot_download('${EMBED_MODEL}', cache_dir='/opt/fastembed-cache/ms')" \
    && chmod -R a+rX /opt/fastembed-cache || \
    echo "[build] 模型预下载失败，运行时将降级关键词匹配（不影响构建）"

# 4) 流水线源码与 scopes（产物目录运行时由卷挂载/生成，已在 .dockerignore 排除）
COPY pipeline/ ./pipeline/
COPY scopes/ ./scopes/
COPY server/ ./server/
# 一键单测：离线、确定、秒级的核心逻辑测试（不联网、不调 API），随镜像分发
COPY tests/ ./tests/
COPY pytest.ini ./pytest.ini
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 5) 非 root 运行用户（缩小被攻破影响面；根治产物被 root 占有的问题）。
#    入口脚本以 root 起、修正卷属主后 setpriv 降到该用户；故镜像默认仍 root 启动，
#    由 entrypoint 完成降权。app 用户家目录给 npm/playwright 缓存用。
#    预建 .npm/.cache 并置 HOME：npm 默认用 $HOME/.npm，若 HOME 缺失/不可写会
#    EACCES（setpriv 不重置 HOME，故这里与 entrypoint 双保险）。
RUN groupadd -g 1000 app && useradd -u 1000 -g 1000 -m -s /bin/bash app \
    && mkdir -p /home/app/.npm /home/app/.cache \
    && chown -R app:app /app /home/app

ENV HOME=/home/app \
    NPM_CONFIG_CACHE=/home/app/.npm \
    # 关掉 stdout 块缓冲：非 TTY（docker logs 管道）下 print 不及时刷新，
    # 会让 worker 启动/进度日志「消失」直到缓冲填满。统一行缓冲，日志即时可见。
    PYTHONUNBUFFERED=1

WORKDIR /app/pipeline

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
# 工具型镜像，不设固定入口命令，运行时按需传命令（用法见 README Docker 章节）
CMD ["python", "-c", "print('web-clone-eval image ready. 用法见 README Docker 章节。')"]
