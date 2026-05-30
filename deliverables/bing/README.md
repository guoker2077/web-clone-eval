# 复刻产物：必应搜索

- 原始网址：https://www.bing.com
- 复刻范围：搜索输入框、搜索提交按钮、搜索结果列表/结果文案区域、结果列表下一页翻页按钮、在输入框填入关键词并点击搜索按钮，结果区域出现且包含关键词、搜索后点击下一页，结果区域刷新并依然可见
- 最佳精修轮：round2
- 一致性总分：**67.5/100**（视觉 58.6 / 功能 75.0 / 交互 70.0）

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
