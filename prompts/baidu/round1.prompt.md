你是资深前端工程师。请复刻目标网页「百度首页」(https://www.baidu.com)。
我会提供原页的整页截图、提取的配色/字体信息，以及需要复刻的功能点。

## 复刻范围（只需实现以下功能点，不要多做）
  - [search-input] (element) 顶部搜索输入框，可聚焦输入文字  原选择器提示: #chat-textarea, #kw, input[name=wd], textarea
  - [search-button] (element) 搜索按钮（百度一下），点击触发搜索  原选择器提示: #su, .s_btn, button[type=submit]
  - [search-submit] (behavior) 在输入框输入关键词后点击搜索按钮，结果区出现与关键词相关的结果文案
  - [result-list] (element) 搜索结果列表，每条含标题与摘要文案
  - [pagination] (behavior) 结果列表底部翻页控件，可点击下一页加载下一批结果

## 原页视觉信息（供还原参考）
- 主要文字色: ['rgb(0, 0, 0)', 'rgb(34, 34, 34)', 'rgb(0, 0, 238)', 'rgb(51, 51, 51)', 'rgb(187, 187, 187)', 'rgb(255, 255, 255)', 'rgb(145, 149, 163)', 'rgb(254, 45, 70)']
- 主要背景色: ['rgb(255, 255, 255)', 'rgb(246, 247, 254)', 'rgb(251, 251, 251)', 'rgb(78, 110, 242)', 'rgb(255, 69, 91)', 'rgb(255, 102, 0)']
- 字体族: ['Arial, sans-serif', '"PingFang SC", Arial, sans-serif', 'arial', 'cIconfont', '"Times New Roman"']
- 字号: ['12px', '14px', '16px', '13px', '18px', '17px', '15px']

## 上一轮评估反馈（必须针对性修正）
上一轮总分 79.2/100，各维度：
- 视觉 79.6, 功能 83.3, 交互 70.0
- 以下元素缺失或不可见: ['result-list']，请补上并标注 data-testid="<功能点id>"。
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