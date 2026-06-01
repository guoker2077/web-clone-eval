# 并发执行验证（WORKER_CONCURRENCY=2）

worker 启动日志：
```
[worker] 43245f3546c1-1-a157 上线，轮询间隔 2.0s，job 超时 1800.0s，并发度=2，沙箱模式=subprocess
```

连续提交两个任务，二者同时进入 running（非排队串行）：

| 时刻 | job1 (github) | job2 (baidu) |
| --- | --- | --- |
| 18:31:05 | running/generating | running/generating |
| 18:31:34 | running/evaluating | running/generating |
| 18:31:58 | running/evaluating | running/generating |

终态与时间（关键证据：started 同一时刻、finished 仅差 3s、各约 170s）：

| 任务 | 状态 | 得分 | started | finished | 用时 |
| --- | --- | --- | --- | --- | --- |
| job1 github | done | 71.3 | 1780309782 | 1780309953 | 171s |
| job2 baidu  | done | 79.6 | 1780309782 | 1780309950 | 168s |

**结论**：两任务 started 时间戳完全相同、全程重叠运行。串行需 ~340s（两任务相加），
并发实际 ~171s，吞吐提升约 2×，与并发度=2 一致。证明主循环并发逻辑端到端生效。
