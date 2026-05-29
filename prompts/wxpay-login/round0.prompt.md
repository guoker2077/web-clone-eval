你是资深前端工程师。请复刻目标网页「微信支付商户登录页」(https://pay.weixin.qq.com/index.php/core/home/login)。
我会提供原页的整页截图、提取的配色/字体信息，以及需要复刻的功能点。

## 复刻范围（只需实现以下功能点，不要多做）
  - [username] (element) 登录账号输入框，placeholder 为「登录账号」  原选择器提示: #idUserName, input[name=username]
  - [password] (element) 登录密码输入框，type=password，placeholder 为「登录密码」  原选择器提示: #idPassword, input[name=password]
  - [captcha-input] (element) 验证码输入框，placeholder 为「验证码」，右侧配验证码图片  原选择器提示: input[name=checkword_in]
  - [captcha-image] (element) 验证码图片，点击可刷新  原选择器提示: img[src*=captcha], .verify-code img
  - [login-button] (element) 登录按钮（账号登录），点击触发表单校验  原选择器提示: .btn_login, a.login, button[type=submit]
  - [fill-and-login] (behavior) 依次填入账号、密码、验证码后点击登录，按钮可点且触发校验反馈

## 原页视觉信息（供还原参考）
- 主要文字色: ['rgb(51, 51, 51)', 'rgb(0, 0, 0)', 'rgb(255, 255, 255)', 'rgb(0, 194, 80)', 'rgb(157, 157, 157)', 'rgb(153, 153, 153)', 'rgba(0, 0, 0, 0.9)']
- 主要背景色: ['rgb(255, 255, 255)', 'rgb(232, 232, 232)', 'rgb(0, 0, 0)', 'rgb(64, 67, 67)', 'rgb(254, 253, 251)', 'rgb(245, 241, 206)', 'rgb(0, 194, 80)', 'rgb(247, 246, 242)']
- 字体族: ['"Helvetica Neue", "Hiragino Sans GB", "Microsoft YaHei", 黑体, Arial, sans-serif', 'Arial', '"Times New Roman"', 'PingFangSC-Medium']
- 字号: ['14px', '12px', '18px', '13px', '16px', '28px', '60px', '20px']

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