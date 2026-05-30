# 复刻产物：GitHub 登录页

- 原始网址：https://github.com/login
- 复刻范围：用户名/邮箱输入框、密码输入框、Sign in 登录按钮、填入用户名和密码并点击 Sign in 登录、空表单直接点击登录，触发必填校验，表单不提交、输入框仍可见
- 最佳精修轮：round0
- 一致性总分：**92.8/100**（视觉 87.0 / 功能 100.0 / 交互 90.0）

## 目录说明

- `source/` —— 完整可维护源码（React + TypeScript + Vite 工程）。
- `dist/` —— 已构建的静态产物，零依赖，可独立运行。

## 独立运行

方式一（直接看产物，无需 Node）：
```bash
cd dist && python3 -m http.server 8080   # 浏览器打开 http://localhost:8080
```

方式二（从源码重新构建）：
```bash
cd source && npm install && npm run build  # 产物在 source/dist/
npm run dev                                 # 或本地开发预览
```

## 说明

- 搜索结果等动态内容为 **mock 数据**（`source/src/mockData.ts`）：复刻目标是结果区域的展示与交互逻辑，不代理真实后端，故以本地假数据呈现。
