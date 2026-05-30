你是资深前端工程师。请复刻目标网页「MDN <a> 元素文档页」(https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a)。
我会提供原页的整页截图、提取的配色/字体信息，以及需要复刻的功能点。

## 复刻范围（只需实现以下功能点，不要多做）
  - [skip-to-content] (element) 顶部「Skip to main content」跳转链接  原选择器提示: a[href="#content"], a
  - [logo-home] (element) 顶部导航栏 MDN 站点 logo（返回首页链接）  原选择器提示: a[href="/en-US/"], a
  - [nav-html-menu] (element) 顶部导航栏「HTML」分类菜单按钮  原选择器提示: button[type="button"]
  - [nav-learn-menu] (element) 顶部导航栏「Learn」分类菜单按钮  原选择器提示: button[type="button"]
  - [nav-blog] (element) 顶部导航栏「Blog」链接  原选择器提示: a[href="/en-US/blog/"], a
  - [breadcrumb-web] (element) 面包屑导航「Web」链接  原选择器提示: a[href="/en-US/docs/Web"], a
  - [breadcrumb-html] (element) 面包屑导航「HTML」链接  原选择器提示: a[href="/en-US/docs/Web/HTML"], a
  - [breadcrumb-reference] (element) 面包屑导航「Reference」链接  原选择器提示: a[href="/en-US/docs/Web/HTML/Reference"], a
  - [breadcrumb-elements] (element) 面包屑导航「Elements」链接  原选择器提示: a[href="/en-US/docs/Web/HTML/Reference/Elements"], a
  - [breadcrumb-anchor] (element) 面包屑导航当前页「<a>」链接  原选择器提示: a[href="/en-US/docs/Web/HTML/Reference/Elements/a"], a
  - [toc-try-it] (element) 右侧 On this page 大纲「Try it」锚点  原选择器提示: a[href="#try_it"], a
  - [toc-attributes] (element) 右侧大纲「Attributes」锚点  原选择器提示: a[href="#attributes"], a
  - [toc-accessibility] (element) 右侧大纲「Accessibility」锚点  原选择器提示: a[href="#accessibility"], a
  - [toc-examples] (element) 右侧大纲「Examples」锚点  原选择器提示: a[href="#examples"], a
  - [toc-security-privacy] (element) 右侧大纲「Security and privacy」锚点  原选择器提示: a[href="#security_and_privacy"], a
  - [toc-technical-summary] (element) 右侧大纲「Technical summary」锚点  原选择器提示: a[href="#technical_summary"], a
  - [toc-specifications] (element) 右侧大纲「Specifications」锚点  原选择器提示: a[href="#specifications"], a
  - [toc-browser-compatibility] (element) 右侧大纲「Browser compatibility」锚点  原选择器提示: a[href="#browser_compatibility"], a
  - [toc-see-also] (element) 右侧大纲「See also」锚点  原选择器提示: a[href="#see_also"], a
  - [content-global-attributes] (element) 正文中「global attributes」链接  原选择器提示: a[href="/en-US/docs/Web/HTML/Reference/Global_attributes"], a
  - [content-attr-download] (element) Attributes 章节内「download」属性锚点链接  原选择器提示: a[href="#download"], a
  - [content-attr-hreflang] (element) Attributes 章节内「hreflang」属性锚点链接  原选择器提示: a[href="#hreflang"], a
  - [header-visible] (behavior) 校验顶部导航栏关键元素渲染可见
  - [breadcrumb-check] (behavior) 校验面包屑层级与当前页标识
  - [toc-jump-attributes] (behavior) 点击右侧大纲 Attributes 锚点后定位到属性章节内容
  - [toc-content-check] (behavior) 校验右侧本页大纲条目文本

## 原页视觉信息（供还原参考）
- 主要文字色: ['rgb(0, 0, 0)', 'rgb(81, 86, 93)', 'rgb(4, 76, 159)', 'rgb(237, 238, 240)']
- 主要背景色: ['rgb(255, 255, 255)', 'rgb(247, 247, 248)', 'rgb(236, 244, 254)', 'rgb(237, 238, 240)', 'rgb(230, 244, 234)', 'rgb(81, 86, 93)', 'rgb(206, 234, 214)', 'rgb(0, 0, 0)']
- 字体族: ['Inter, sans-serif', '"JetBrains Mono", monospace']
- 字号: ['16px', '24px', '32px', '20px', '40px']

## 上一轮评估反馈（必须针对性修正）
上一轮总分 80.2/100，各维度：
- 视觉 50.6, 功能 100.0, 交互 100.0
- [desktop] 视觉结构相似度偏低 (SSIM=0.5801)，像素差异 0.1212，请更贴近原页布局与配色。
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