===FILE: package.json===
```json
{
  "name": "wechat-pay-merchant-login",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "typescript": "^5.5.3",
    "vite": "^5.4.0"
  }
}
```

===FILE: vite.config.ts===
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

===FILE: tsconfig.json===
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

===FILE: tsconfig.node.json===
```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noEmit": true
  },
  "include": ["vite.config.ts"]
}
```

===FILE: index.html===
```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>微信支付商户平台 - 商户登录</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

===FILE: src/main.tsx===
```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
)
```

===FILE: src/index.css===
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  height: 100%;
}

body {
  font-family: 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', 黑体,
    Arial, sans-serif;
  color: rgb(51, 51, 51);
  background-color: rgb(247, 246, 242);
  -webkit-font-smoothing: antialiased;
}

#root {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

input {
  font-family: inherit;
}

button {
  font-family: inherit;
  cursor: pointer;
}
```

===FILE: src/App.tsx===
```tsx
import Header from './components/Header'
import LoginCard from './components/LoginCard'
import Footer from './components/Footer'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <Header />
      <main className="login-main">
        <div className="login-banner-text">
          <h1>微信支付商户平台</h1>
          <p>专业、安全、便捷的商户经营服务</p>
        </div>
        <LoginCard />
      </main>
      <Footer />
    </div>
  )
}
```

===FILE: src/App.css===
```css
.app {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.login-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
  padding: 70px 24px;
  gap: 40px;
  flex-wrap: wrap;
}

.login-banner-text {
  flex: 1;
  min-width: 320px;
}

.login-banner-text h1 {
  font-size: 36px;
  font-weight: 500;
  color: rgb(51, 51, 51);
  letter-spacing: 1px;
}

.login-banner-text p {
  margin-top: 16px;
  font-size: 16px;
  color: rgb(153, 153, 153);
}
```

===FILE: src/components/Header.tsx===
```tsx
import './Header.css'

export default function Header() {
  return (
    <header className="site-header">
      <div className="header-inner">
        <a className="brand" href="#">
          <span className="brand-logo" aria-hidden="true">
            <svg viewBox="0 0 1024 1024" width="36" height="36">
              <circle cx="512" cy="512" r="512" fill="#00C250" />
              <path
                d="M300 430c0-78 80-138 178-138 88 0 161 48 175 113-6-1-12-1-18-1-110 0-200 74-200 165 0 16 3 31 8 45-7 1-15 1-23 1-26 0-51-4-73-11l-58 31 16-54c-43-31-70-78-70-130 0-22 1-22 1-31z"
                fill="#fff"
              />
              <path
                d="M760 600c0-72-72-130-160-130s-160 58-160 130 72 130 160 130c20 0 39-3 56-8l46 25-13-43c34-26 71-56 71-104z"
                fill="#fff"
              />
            </svg>
          </span>
          <span className="brand-text">微信支付</span>
        </a>
        <nav className="header-nav">
          <a href="#" className="active">
            首页
          </a>
          <a href="#">产品中心</a>
          <a href="#">服务市场</a>
          <a href="#">帮助中心</a>
          <a href="#">联系我们</a>
        </nav>
        <button className="header-cta" type="button">
          成为服务商
        </button>
      </div>
    </header>
  )
}
```

===FILE: src/components/Header.css===
```css
.site-header {
  background-color: rgb(255, 255, 255);
  border-bottom: 1px solid rgb(232, 232, 232);
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-inner {
  max-width: 1180px;
  margin: 0 auto;
  height: 64px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.brand-logo {
  display: inline-flex;
  width: 36px;
  height: 36px;
}

.brand-text {
  font-size: 20px;
  font-weight: 500;
  color: rgb(51, 51, 51);
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 36px;
  margin-left: auto;
}

.header-nav a {
  font-size: 14px;
  color: rgb(51, 51, 51);
  text-decoration: none;
  padding: 6px 0;
  position: relative;
}

.header-nav a:hover {
  color: rgb(0, 194, 80);
}

.header-nav a.active {
  color: rgb(0, 194, 80);
}

.header-nav a.active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -8px;
  height: 2px;
  background-color: rgb(0, 194, 80);
}

.header-cta {
  background-color: rgb(0, 194, 80);
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 9px 18px;
  font-size: 14px;
}

.header-cta:hover {
  background-color: rgb(2, 173, 72);
}
```

===FILE: src/components/LoginCard.tsx===
```tsx
import { useMemo, useState } from 'react'
import './LoginCard.css'

type FieldErrors = {
  username?: string
  password?: string
  captcha?: string
}

function makeCaptcha(): string {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let result = ''
  for (let i = 0; i < 4; i++) {
    result += chars[Math.floor(Math.random() * chars.length)]
  }
  return result
}

export default function LoginCard() {
  const [tab, setTab] = useState<'account' | 'qrcode'>('account')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [captchaInput, setCaptchaInput] = useState('')
  const [captcha, setCaptcha] = useState(makeCaptcha)
  const [errors, setErrors] = useState<FieldErrors>({})
  const [status, setStatus] = useState<string>('')

  const captchaSvg = useMemo(() => {
    const colors = ['#333', '#00C250', '#9d9d9d', '#404343']
    const glyphs = captcha.split('').map((c, i) => {
      const x = 14 + i * 24
      const y = 28 + (Math.random() * 6 - 3)
      const rotate = Math.random() * 30 - 15
      const fill = colors[Math.floor(Math.random() * colors.length)]
      return `<text x="${x}" y="${y}" font-size="22" font-family="Arial" font-weight="bold" fill="${fill}" transform="rotate(${rotate} ${x} ${y})">${c}</text>`
    })
    const lines = Array.from({ length: 4 }, () => {
      const x1 = Math.random() * 110
      const y1 = Math.random() * 40
      const x2 = Math.random() * 110
      const y2 = Math.random() * 40
      return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#cdcdcd" stroke-width="1"/>`
    })
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="110" height="40" viewBox="0 0 110 40"><rect width="110" height="40" fill="#f5f1ce"/>${lines.join(
      ''
    )}${glyphs.join('')}</svg>`
    return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
  }, [captcha])

  function refreshCaptcha() {
    setCaptcha(makeCaptcha())
    setCaptchaInput('')
  }

  function validate(): FieldErrors {
    const next: FieldErrors = {}
    if (!username.trim()) next.username = '请输入登录账号'
    if (!password) next.password = '请输入登录密码'
    if (!captchaInput.trim()) {
      next.captcha = '请输入验证码'
    } else if (
      captchaInput.trim().toUpperCase() !== captcha.toUpperCase()
    ) {
      next.captcha = '验证码错误'
    }
    return next
  }

  function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setStatus('')
    const next = validate()
    setErrors(next)
    if (Object.keys(next).length > 0) {
      refreshCaptcha()
      return
    }
    setStatus('success')
  }

  return (
    <section className="login-card" data-testid="login-card">
      <div className="login-tabs">
        <button
          type="button"
          className={tab === 'account' ? 'tab active' : 'tab'}
          onClick={() => setTab('account')}
        >
          账号登录
        </button>
        <button
          type="button"
          className={tab === 'qrcode' ? 'tab active' : 'tab'}
          onClick={() => setTab('qrcode')}
        >
          扫码登录
        </button>
      </div>

      {tab === 'account' ? (
        <form className="login-form" onSubmit={handleLogin} noValidate>
          <div className="field">
            <input
              id="idUserName"
              name="username"
              type="text"
              placeholder="登录账号"
              data-testid="username"
              className={errors.username ? 'input error' : 'input'}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            {errors.username && (
              <span className="field-error">{errors.username}</span>
            )}
          </div>

          <div className="field">
            <input
              id="idPassword"
              name="password"
              type="password"
              placeholder="登录密码"
              data-testid="password"
              className={errors.password ? 'input error' : 'input'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {errors.password && (
              <span className="field-error">{errors.password}</span>
            )}
          </div>

          <div className="field">
            <div className="captcha-row">
              <input
                name="checkword_in"
                type="text"
                placeholder="验证码"
                data-testid="captcha-input"
                className={errors.captcha ? 'input error' : 'input'}
                value={captchaInput}
                onChange={(e) => setCaptchaInput(e.target.value)}
                autoComplete="off"
              />
              <img
                className="captcha-image"
                src={captchaSvg}
                alt="点击刷新验证码"
                title="点击刷新验证码"
                data-testid="captcha-image"
                onClick={refreshCaptcha}
              />
            </div>
            {errors.captcha && (
              <span className="field-error">{errors.captcha}</span>
            )}
          </div>

          <button
            type="submit"
            className="btn_login"
            data-testid="login-button"
          >
            登录
          </button>

          {status === 'success' && (
            <div className="login-success" data-testid="login-success">
              登录成功，正在进入商户平台...
            </div>
          )}

          <div className="login-extra">
            <a href="#">忘记密码？</a>
            <a href="#">注册新账号</a>
          </div>
        </form>
      ) : (
        <div className="qrcode-pane">
          <div className="qrcode-box" aria-hidden="true">
            <svg viewBox="0 0 100 100" width="160" height="160">
              <rect width="100" height="100" fill="#fff" />
              <g fill="#333">
                <rect x="6" y="6" width="22" height="22" />
                <rect x="12" y="12" width="10" height="10" fill="#fff" />
                <rect x="72" y="6" width="22" height="22" />
                <rect x="78" y="12" width="10" height="10" fill="#fff" />
                <rect x="6" y="72" width="22" height="22" />
                <rect x="12" y="78" width="10" height="10" fill="#fff" />
                <rect x="40" y="40" width="8" height="8" />
                <rect x="52" y="40" width="8" height="8" />
                <rect x="40" y="52" width="8" height="8" />
                <rect x="60" y="60" width="8" height="8" />
                <rect x="72" y="44" width="8" height="8" />
                <rect x="44" y="72" width="8" height="8" />
              </g>
            </svg>
          </div>
          <p className="qrcode-tip">
            请使用微信支付商家助手小程序扫码登录
          </p>
        </div>
      )}
    </section>
  )
}
```

===FILE: src/components/LoginCard.css===
```css
.login-card {
  width: 380px;
  background-color: rgb(255, 255, 255);
  border: 1px solid rgb(232, 232, 232);
  border-radius: 8px;
  padding: 32px 36px 36px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.06);
}

.login-tabs {
  display: flex;
  border-bottom: 1px solid rgb(232, 232, 232);
  margin-bottom: 28px;
}

.login-tabs .tab {
  flex: 1;
  background: none;
  border: none;
  padding: 12px 0;
  font-size: 16px;
  color: rgb(153, 153, 153);
  position: relative;
}

.login-tabs .tab.active {
  color: rgb(51, 51, 51);
  font-weight: 500;
}

.login-tabs .tab.active::after {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: -1px;
  width: 40px;
  height: 2px;
  background-color: rgb(0, 194, 80);
}

.login-form {
  display: flex;
  flex-direction: column;
}

.field {
  margin-bottom: 18px;
}

.input {
  width: 100%;
  height: 44px;
  border: 1px solid rgb(232, 232, 232);
  border-radius: 4px;
  padding: 0 12px;
  font-size: 14px;
  color: rgb(51, 51, 51);
  outline: none;
  transition: border-color 0.15s;
}

.input::placeholder {
  color: rgb(157, 157, 157);
}

.input:focus {
  border-color: rgb(0, 194, 80);
}

.input.error {
  border-color: #e64340;
}

.captcha-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.captcha-row .input {
  flex: 1;
}

.captcha-image {
  width: 110px;
  height: 44px;
  border: 1px solid rgb(232, 232, 232);
  border-radius: 4px;
  cursor: pointer;
  display: block;
  flex-shrink: 0;
}

.field-error {
  display: block;
  margin-top: 6px;
  font-size: 12px;
  color: #e64340;
}

.btn_login {
  width: 100%;
  height: 44px;
  background-color: rgb(0, 194, 80);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  margin-top: 6px;
  transition: background-color 0.15s;
}

.btn_login:hover {
  background-color: rgb(2, 173, 72);
}

.btn_login:active {
  background-color: rgb(0, 168, 70);
}

.login-success {
  margin-top: 14px;
  padding: 10px 12px;
  background-color: rgb(245, 241, 206);
  color: rgb(51, 51, 51);
  border-radius: 4px;
  font-size: 13px;
  text-align: center;
}

.login-extra {
  display: flex;
  justify-content: space-between;
  margin-top: 18px;
}

.login-extra a {
  font-size: 13px;
  color: rgb(153, 153, 153);
  text-decoration: none;
}

.login-extra a:hover {
  color: rgb(0, 194, 80);
}

.qrcode-pane {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 0 24px;
}

.qrcode-box {
  width: 180px;
  height: 180px;
  border: 1px solid rgb(232, 232, 232);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qrcode-tip {
  margin-top: 18px;
  font-size: 13px;
  color: rgb(153, 153, 153);
}
```

===FILE: src/components/Footer.tsx===
```tsx
import './Footer.css'

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div className="footer-links">
          <div className="footer-col">
            <h4>产品中心</h4>
            <a href="#">付款产品</a>
            <a href="#">营销工具</a>
            <a href="#">行业方案</a>
          </div>
          <div className="footer-col">
            <h4>商户接入</h4>
            <a href="#">接入指引</a>
            <a href="#">服务商入驻</a>
            <a href="#">开发文档</a>
          </div>
          <div className="footer-col">
            <h4>帮助中心</h4>
            <a href="#">常见问题</a>
            <a href="#">联系客服</a>
            <a href="#">投诉建议</a>
          </div>
          <div className="footer-col">
            <h4>关于我们</h4>
            <a href="#">公司介绍</a>
            <span>客服热线：95017-2</span>
            <span>服务时间：09:00-22:00</span>
          </div>
        </div>
      </div>
      <div className="footer-copy">
        Powered By Tencent &amp; Tenpay　Copyright 2005-2026 Tenpay All Rights
        Reserved.
      </div>
    </footer>
  )
}
```

===FILE: src/components/Footer.css===
```css
.site-footer {
  background-color: rgb(64, 67, 67);
  color: rgb(157, 157, 157);
  margin-top: auto;
}

.footer-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px 24px;
}

.footer-links {
  display: flex;
  gap: 80px;
  flex-wrap: wrap;
}

.footer-col {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-col h4 {
  color: rgb(255, 255, 255);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.footer-col a,
.footer-col span {
  color: rgb(157, 157, 157);
  font-size: 13px;
  text-decoration: none;
}

.footer-col a:hover {
  color: rgb(255, 255, 255);
}

.footer-copy {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  font-size: 12px;
  color: rgb(157, 157, 157);
  padding: 18px 24px;
}
```