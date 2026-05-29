你是资深前端工程师。请复刻目标网页「GitHub 登录页」(https://github.com/login)。
我会提供原页的整页截图、提取的配色/字体信息，以及需要复刻的功能点。

## 复刻范围（只需实现以下功能点，不要多做）
  - [username] (element) Username or email address 输入框  原选择器提示: #login_field, input[name=login]
  - [password] (element) Password 输入框，type=password，上方有 Forgot password 链接  原选择器提示: #password, input[name=password]
  - [submit-button] (element) Sign in 登录按钮，绿色，整行宽度  原选择器提示: input[type=submit][name=commit], button[type=submit], .btn-primary
  - [signup-link] (element) 底部 Create an account 注册引导链接  原选择器提示: a[href*=signup]
  - [login-flow] (behavior) 填入用户名密码后点击 Sign in，按钮可点击并触发表单提交校验
  - [empty-validation] (behavior) 不填任何内容直接点击登录，应有必填校验反馈（HTML5 required 或自定义提示）

## 原页视觉信息（供还原参考）
- 主要文字色: ['rgb(31, 35, 40)', 'rgb(0, 0, 0)', 'rgb(37, 41, 46)', 'rgb(9, 105, 218)', 'rgb(255, 255, 255)', 'rgb(89, 99, 110)']
- 主要背景色: ['rgb(255, 255, 255)', 'rgb(246, 248, 250)', 'rgb(31, 136, 61)']
- 字体族: ['"Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"', 'sans-serif']
- 字号: ['14px', '12px', '16px', '20px']

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

## 输出格式（严格遵守）
对每个文件，先输出一行 `===FILE: 相对路径===`，紧接其完整内容。
必须包含: package.json、vite.config.ts、index.html、src/main.tsx、src/App.tsx 及所需样式/组件。
package.json 的 scripts 至少含 dev/build/preview，依赖只用 react/react-dom + vite + @vitejs/plugin-react + typescript。
现在开始输出工程文件：