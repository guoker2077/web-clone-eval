你是资深前端工程师。请复刻目标网页「必应搜索」(https://www.bing.com)。
我会提供原页的整页截图、提取的配色/字体信息，以及需要复刻的功能点。

## 复刻范围（只需实现以下功能点，不要多做）
  - [search-input] (element) 搜索输入框  原选择器提示: #sb_form_q, input[name=q]
  - [search-button] (element) 搜索提交按钮  原选择器提示: #sb_form_go, label[for=sb_form_go], #search_icon
  - [search-results] (element) 搜索结果列表/结果文案区域  原选择器提示: #b_results, .b_algo, ol#b_results
  - [next-page] (element) 结果列表下一页翻页按钮  原选择器提示: a.sb_pagN, a[title='下一页'], a[aria-label='下一页']
  - [search-flow] (behavior) 在输入框填入关键词并点击搜索按钮，结果区域出现且包含关键词
  - [pagination-flow] (behavior) 搜索后点击下一页，结果区域刷新并依然可见

## 原页视觉信息（供还原参考）
- 主要文字色: ['rgb(17, 17, 17)', 'rgb(0, 0, 0)', 'rgb(43, 43, 43)', 'rgb(255, 255, 255)', 'rgb(221, 221, 221)', 'rgba(255, 255, 255, 0.8)', 'rgb(76, 76, 76)', 'rgb(34, 34, 34)']
- 主要背景色: ['rgb(85, 85, 85)', 'rgba(255, 255, 255, 0.7)', 'rgba(34, 34, 34, 0.9)', 'rgb(255, 255, 255)', 'rgb(236, 236, 236)']
- 字体族: ['"Segoe UI", Segoe, Tahoma, Arial, Verdana, sans-serif', 'Arial', '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif']
- 字号: ['16px', '13px', '12.8px', '14px']

## 上一轮评估反馈（必须针对性修正）
上一轮总分 62.9/100，各维度：
- 视觉 47.2, 功能 75.0, 交互 70.0
- [desktop] 视觉结构相似度偏低 (SSIM=0.4214)，像素差异 0.7955，请更贴近原页布局与配色。
- 以下元素缺失或不可见: ['search-results', 'next-page']，请补上并标注 data-testid="<功能点id>"。
请重点修复上述低分维度与失败的交互断言。

## 技术要求
1. 用 Vite + React + TypeScript 工程，可 `npm install && npm run build` 构建。
2. 视觉上尽量贴近截图：布局、配色、字体、间距、组件样式。
3. 交互功能点必须真实可用（输入、点击、状态变化、翻页等），数据可用本地 mock。
4. **关键**：为可测试的交互元素加稳定的 `data-testid`，命名用功能点 id（如 data-testid="search-input"）。
   翻页的下一页按钮用 data-testid="next-page"，结果列表用 data-testid="result-list"。
5. 工程自包含，不依赖外部 CDN（字体除外可降级到系统字体）。
6. 不要写任何解释文字，只输出文件。

## 构建必须成功（极重要，否则本轮作废）
- package.json 的 build 脚本只用 `vite build`，**不要**用 `tsc && vite build`（避免类型检查中断构建）。
- tsconfig.json 设 `"noUnusedLocals": false`、`"noUnusedParameters": false`，避免未使用变量导致失败。
- 所有 import 必须真实存在；所有用到的变量/类型都要定义；不要留半成品代码。
- React 18 写法，import 用 `import { useState } from 'react'`。

## 样式必须真正生效（极重要，否则视觉全错）
- 每个 `.css` 文件都必须被某个 `.tsx`/`.ts` 文件 `import`（如 `import './styles.css'`），
  否则 Vite 不会打包它，页面退化成浏览器默认样式（label 与 input 挤同行、按钮变小、布局错乱）。
- 不要生成"孤儿 CSS"：写了样式文件却没人 import。每写一个样式文件，就在对应组件顶部加上它的 import。
- 不要写空的或只有注释的 CSS 文件来占位。

## 输出格式（严格遵守）
对每个文件，先输出一行 `===FILE: 相对路径===`，紧接其完整内容。
必须包含: package.json、vite.config.ts、index.html、src/main.tsx、src/App.tsx 及所需样式/组件。
package.json 的 scripts 至少含 dev/build/preview，依赖只用 react/react-dom + vite + @vitejs/plugin-react + typescript。
现在开始输出工程文件：