#!/bin/sh
# 容器入口：以 root 启动时先修正挂载卷属主，再降权到非 root 的 app 用户运行。
#
# 为什么需要：output/reports/prompts/scopes/data 这些目录由宿主机 bind-mount 进来，
# 属主是宿主机用户。容器内 app 用户（UID=$APP_UID）要能写它们，必须先 chown；
# 否则要么写不进去，要么（容器是 root 时）写出去的产物在宿主机上是 root 属主、
# 宿主机普通用户删不掉——这正是之前踩过的坑。修正后降权，让真正干活（尤其是
# 抓取陌生人页面）的进程不是 root，缩小被攻破后的影响面。
#
# 关键：setpriv 不会重置 HOME（不像 su/sudo -i），若不显式设置，root 的
# HOME=/root 会原样带给 app 用户，导致 npm 去写 /root/.npm 触发 EACCES。
# 故降权时把 HOME 指到 app 家目录，让 npm/playwright 缓存落到可写位置。
set -e

APP_UID="${APP_UID:-1000}"
APP_GID="${APP_GID:-1000}"
APP_HOME="${APP_HOME:-/home/app}"

if [ "$(id -u)" = "0" ]; then
    for d in /app/output /app/reports /app/prompts /app/scopes /app/data; do
        [ -d "$d" ] && chown -R "${APP_UID}:${APP_GID}" "$d" 2>/dev/null || true
    done
    # 降权执行实际命令（setpriv 来自 util-linux，基础镜像自带）。
    # 显式置 HOME，否则 npm/playwright 会去写 root 家目录（EACCES）。
    export HOME="$APP_HOME"
    exec setpriv --reuid "$APP_UID" --regid "$APP_GID" --init-groups \
        env "HOME=$APP_HOME" "$@"
fi

# 已是非 root（如 compose 里显式指定了 user）：直接执行
exec "$@"

