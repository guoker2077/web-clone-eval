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
    PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright

# 1) 系统依赖 + Node.js + 中文字体
#    - curl/gnupg：装 NodeSource
#    - fonts-noto-cjk：CJK 字体，修复截图方框
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl gnupg ca-certificates fontconfig fonts-noto-cjk \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && fc-cache -f \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Python 依赖（先拷 requirements，利用层缓存）
COPY requirements.txt ./
RUN pip install -r requirements.txt

# 3) Playwright Chromium 及其运行所需系统库
#    playwright install --with-deps 会自动补齐 Chromium 的系统依赖
RUN playwright install --with-deps chromium

# 4) 流水线源码与 scopes（产物目录运行时由卷挂载/生成，已在 .dockerignore 排除）
COPY pipeline/ ./pipeline/
COPY scopes/ ./scopes/

WORKDIR /app/pipeline

# 工具型镜像，不设固定入口，运行时按需传命令（用法见 README Docker 章节）
CMD ["python", "-c", "print('web-clone-eval image ready. 用法见 README Docker 章节。')"]
