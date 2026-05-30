# 复刻产物：MDN <a> 元素文档页

- 原始网址：https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a
- 复刻范围：顶部「Skip to main content」跳转链接、顶部导航栏 MDN 站点 logo（返回首页链接）、顶部导航栏「HTML」分类菜单按钮、顶部导航栏「Learn」分类菜单按钮、顶部导航栏「Blog」链接、面包屑导航「Web」链接、面包屑导航「HTML」链接、面包屑导航「Reference」链接、面包屑导航「Elements」链接、面包屑导航当前页「<a>」链接、右侧 On this page 大纲「Try it」锚点、右侧大纲「Attributes」锚点、右侧大纲「Accessibility」锚点、右侧大纲「Examples」锚点、右侧大纲「Security and privacy」锚点、右侧大纲「Technical summary」锚点、右侧大纲「Specifications」锚点、右侧大纲「Browser compatibility」锚点、右侧大纲「See also」锚点、正文中「global attributes」链接、Attributes 章节内「download」属性锚点链接、Attributes 章节内「hreflang」属性锚点链接、校验顶部导航栏关键元素渲染可见、校验面包屑层级与当前页标识、点击右侧大纲 Attributes 锚点后定位到属性章节内容、校验右侧本页大纲条目文本
- 最佳精修轮：round0
- 一致性总分：**80.2/100**（视觉 50.6 / 功能 100.0 / 交互 100.0）

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
