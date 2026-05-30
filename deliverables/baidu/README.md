# 复刻产物：百度首页

- 原始网址：https://www.baidu.com
- 复刻范围：顶部搜索输入框，可聚焦输入文字、搜索按钮（百度一下），点击触发搜索、在输入框输入关键词后点击搜索按钮，结果区出现与关键词相关的结果文案、搜索结果列表，每条含标题与摘要文案、结果列表底部翻页控件，可点击下一页加载下一批结果
- 最佳精修轮：round0
- 一致性总分：**79.2/100**（视觉 79.6 / 功能 83.3 / 交互 70.0）

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
