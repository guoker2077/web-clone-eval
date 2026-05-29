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
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}
```

===FILE: vite.config.ts===
```typescript
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
    "noUnusedLocals": false,
    "noUnusedParameters": false
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
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>微信支付商户平台 - 登录</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

===FILE: public/favicon.svg===
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <circle cx="16" cy="16" r="16" fill="#00c250"/>
  <path d="M20 9c-5 0-9 3.4-9 7.6 0 2.4 1.3 4.5 3.4 5.9l-.8 2.5 2.9-1.5c.5.1 1 .1 1.5.1 5 0 9-3.4 9-7.6S25 9 20 9z" fill="#fff"/>
</svg>
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
  color: #333;
  background: #fff;
  -webkit-font-smoothing: antialiased;
}

a {
  text-decoration: none;
  color: inherit;
}

input {
  font-family: inherit;
}

#root {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}
```

===FILE: src/App.tsx===
```tsx
import Header from './components/Header'
import LoginPanel from './components/LoginPanel'
import Footer from './components/Footer'
import './App.css'

export default function App() {
  return (
    <>
      <Header />
      <main className="login-stage">
        <div className="login-stage__inner">
          <div className="login-stage__brand">
            <div className="brand-mark">
              <span className="brand-mark__logo" aria-hidden="true">
                <svg viewBox="0 0 32 32" width="40" height="40">
                  <circle cx="16" cy="16" r="16" fill="#00c250" />
                  <path
                    d="M20 9c-5 0-9 3.4-9 7.6 0 2.4 1.3 4.5 3.4 5.9l-.8 2.5 2.9-1.5c.5.1 1 .1 1.5.1 5 0 9-3.4 9-7.6S25 9 20 9z"
                    fill="#fff"
                  />
                </svg>
              </span>
              <span className="brand-mark__title">微信支付商户平台</span>
            </div>
            <h1 className="brand-headline">让每一笔生意，都有保障</h1>
            <p className="brand-sub">
              安全、稳定、高效的企业级支付服务，助力商家轻松经营。
            </p>
            <ul className="brand-points">
              <li>资金安全有保障</li>
              <li>多种收款方式</li>
              <li>实时对账与报表</li>
            </ul>
          </div>
          <LoginPanel />
        </div>
      </main>
      <Footer />
    </>
  )
}
```

===FILE: src/App.css===
```css
.login-stage {
  flex: 1;
  background: linear-gradient(180deg, #f7f6f2 0%, #e8e8e8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
}

.login-stage__inner {
  width: 100%;
  max-width: 980px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 60px;
}

.login-stage__brand {
  flex: 1;
  max-width: 440px;
  color: #333;
}

.brand-mark {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 36px;
}

.brand-mark__title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.brand-headline {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  line-height: 1.4;
  margin-bottom: 16px;
}

.brand-sub {
  font-size: 14px;
  color: #999;
  line-height: 1.8;
  margin-bottom: 28px;
}

.brand-points {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.brand-points li {
  position: relative;
  padding-left: 24px;
  font-size: 14px;
  color: #666;
}

.brand-points li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #00c250;
  box-shadow: inset 0 0 0 2px #fff;
}

@media (max-width: 820px) {
  .login-stage__inner {
    flex-direction: column;
    gap: 32px;
  }
  .login-stage__brand {
    text-align: center;
    max-width: 100%;
  }
  .brand-mark {
    justify-content: center;
  }
  .brand-points {
    align-items: center;
  }
}
```

===FILE: src/components/Header.tsx===
```tsx
import './Header.css'

const NAV = ['首页', '产品中心', '服务市场', '商户接入', '帮助中心']

export default function Header() {
  return (
    <header className="site-header">
      <div className="site-header__top">
        <div className="site-header__top-inner">
          <span className="top-link active">微信支付</span>
          <span className="top-divider">|</span>
          <span className="top-link">商家产品</span>
          <span className="top-divider">|</span>
          <span className="top-link en">International Business</span>
        </div>
      </div>
      <div className="site-header__main">
        <div className="site-header__main-inner">
          <a className="logo" href="#">
            <span className="logo__icon" aria-hidden="true">
              <svg viewBox="0 0 32 32" width="34" height="34">
                <circle cx="16" cy="16" r="16" fill="#00c250" />
                <path
                  d="M20 9c-5 0-9 3.4-9 7.6 0 2.4 1.3 4.5 3.4 5.9l-.8 2.5 2.9-1.5c.5.1 1 .1 1.5.1 5 0 9-3.4 9-7.6S25 9 20 9z"
                  fill="#fff"
                />
              </svg>
            </span>
            <span className="logo__text">微信支付</span>
          </a>
          <nav className="nav">
            {NAV.map((item, i) => (
              <a key={item} href="#" className={i === 0 ? 'nav__item active' : 'nav__item'}>
                {item}
              </a>
            ))}
          </nav>
          <a className="header-cta" href="#">
            成为商家
          </a>
        </div>
      </div>
    </header>
  )
}
```

===FILE: src/components/Header.css===
```css
.site-header {
  width: 100%;
}

.site-header__top {
  background: #2d3033;
  height: 32px;
}

.site-header__top-inner {
  max-width: 1180px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 12px;
}

.top-link {
  font-size: 12px;
  color: #9d9d9d;
  cursor: pointer;
}

.top-link.active {
  color: #00c250;
}

.top-link.en {
  color: #ccc;
}

.top-divider {
  color: #555;
  font-size: 12px;
}

.site-header__main {
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
}

.site-header__main-inner {
  max-width: 1180px;
  margin: 0 auto;
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo__text {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.nav {
  display: flex;
  align-items: center;
  gap: 40px;
  margin-left: auto;
}

.nav__item {
  font-size: 14px;
  color: #333;
  position: relative;
  padding: 6px 0;
}

.nav__item.active {
  color: #00c250;
}

.nav__item.active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -6px;
  height: 2px;
  background: #00c250;
}

.nav__item:hover {
  color: #00c250;
}

.header-cta {
  margin-left: 48px;
  background: #00c250;
  color: #fff;
  font-size: 14px;
  padding: 9px 22px;
  border-radius: 4px;
  transition: background 0.2s;
}

.header-cta:hover {
  background: #00a847;
}

@media (max-width: 820px) {
  .nav {
    display: none;
  }
  .header-cta {
    margin-left: auto;
  }
}
```

===FILE: src/components/LoginPanel.tsx===
```tsx
import { useMemo, useState } from 'react'
import Captcha from './Captcha'
import './LoginPanel.css'

type Mode = 'account' | 'qr'

export default function LoginPanel() {
  const [mode, setMode] = useState<Mode>('account')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [captcha, setCaptcha] = useState('')
  const [captchaCode, setCaptchaCode] = useState(() => genCode())
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const refreshCaptcha = () => {
    setCaptchaCode(genCode())
    setCaptcha('')
  }

  const handleLogin = () => {
    setSuccess(false)
    if (!username.trim()) {
      setError('请输入登录账号')
      return
    }
    if (!password) {
      setError('请输入登录密码')
      return
    }
    if (!captcha.trim()) {
      setError('请输入验证码')
      return
    }
    if (captcha.trim().toLowerCase() !== captchaCode.toLowerCase()) {
      setError('验证码不正确，请重新输入')
      refreshCaptcha()
      return
    }
    setError('')
    setSuccess(true)
  }

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleLogin()
  }

  const qrPattern = useMemo(() => buildQrPattern(), [])

  return (
    <section className="login-panel" aria-label="登录">
      <div className="login-tabs">
        <button
          className={mode === 'account' ? 'login-tab active' : 'login-tab'}
          onClick={() => setMode('account')}
          type="button"
        >
          账号登录
        </button>
        <button
          className={mode === 'qr' ? 'login-tab active' : 'login-tab'}
          onClick={() => setMode('qr')}
          type="button"
        >
          扫码登录
        </button>
      </div>

      {mode === 'account' ? (
        <div className="login-form">
          <div className="field">
            <input
              id="idUserName"
              name="username"
              data-testid="username"
              className="field__input"
              type="text"
              placeholder="登录账号"
              autoComplete="username"
              value={username}
              onChange={(e) => {
                setUsername(e.target.value)
                setError('')
                setSuccess(false)
              }}
              onKeyDown={onKeyDown}
            />
          </div>

          <div className="field">
            <input
              id="idPassword"
              name="password"
              data-testid="password"
              className="field__input"
              type="password"
              placeholder="登录密码"
              autoComplete="current-password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                setError('')
                setSuccess(false)
              }}
              onKeyDown={onKeyDown}
            />
          </div>

          <div className="field field--captcha">
            <input
              name="checkword_in"
              data-testid="captcha-input"
              className="field__input field__input--captcha"
              type="text"
              placeholder="验证码"
              maxLength={4}
              value={captcha}
              onChange={(e) => {
                setCaptcha(e.target.value)
                setError('')
                setSuccess(false)
              }}
              onKeyDown={onKeyDown}
            />
            <Captcha code={captchaCode} onRefresh={refreshCaptcha} />
          </div>

          {error && (
            <div className="login-msg login-msg--error" data-testid="login-error" role="alert">
              {error}
            </div>
          )}
          {success && (
            <div className="login-msg login-msg--ok" data-testid="login-success" role="status">
              校验通过，正在登录…
            </div>
          )}

          <button
            className="btn_login"
            data-testid="login-button"
            type="button"
            onClick={handleLogin}
          >
            登录
          </button>

          <div className="login-links">
            <a href="#">忘记账号</a>
            <a href="#">忘记密码</a>
            <a href="#" className="login-links__primary">
              注册
            </a>
          </div>
        </div>
      ) : (
        <div className="login-qr">
          <div className="login-qr__code" aria-hidden="true">
            <div className="qr-grid">
              {qrPattern.map((on, i) => (
                <span key={i} className={on ? 'qr-cell on' : 'qr-cell'} />
              ))}
            </div>
          </div>
          <p className="login-qr__tip">请使用微信扫一扫登录</p>
          <p className="login-qr__sub">「微信」&gt; 右上角 + &gt; 扫一扫</p>
        </div>
      )}
    </section>
  )
}

function genCode() {
  const chars = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
  let s = ''
  for (let i = 0; i < 4; i++) {
    s += chars[Math.floor(Math.random() * chars.length)]
  }
  return s
}

function buildQrPattern() {
  const size = 21
  const arr: boolean[] = []
  for (let i = 0; i < size * size; i++) {
    arr.push(Math.random() > 0.5)
  }
  return arr
}
```

===FILE: src/components/LoginPanel.css===
```css
.login-panel {
  width: 360px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  padding: 8px 36px 36px;
  flex-shrink: 0;
}

.login-tabs {
  display: flex;
  gap: 32px;
  border-bottom: 1px solid #eee;
  margin: 0 -36px 28px;
  padding: 24px 36px 0;
}

.login-tab {
  background: none;
  border: none;
  font-size: 16px;
  color: #999;
  cursor: pointer;
  padding: 0 0 16px;
  position: relative;
  font-family: inherit;
}

.login-tab.active {
  color: #333;
  font-weight: 500;
}

.login-tab.active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 2px;
  background: #00c250;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.field {
  margin-bottom: 18px;
}

.field--captcha {
  display: flex;
  gap: 12px;
}

.field__input {
  width: 100%;
  height: 44px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 0 14px;
  font-size: 14px;
  color: #333;
  outline: none;
  transition: border-color 0.2s;
  background: #fff;
}

.field__input::placeholder {
  color: #9d9d9d;
}

.field__input:focus {
  border-color: #00c250;
}

.field__input--captcha {
  flex: 1;
}

.login-msg {
  font-size: 13px;
  margin-bottom: 14px;
  line-height: 1.5;
}

.login-msg--error {
  color: #e64340;
}

.login-msg--ok {
  color: #00c250;
}

.btn_login {
  height: 46px;
  background: #00c250;
  color: #fff;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.2s;
  margin-top: 4px;
}

.btn_login:hover {
  background: #00a847;
}

.btn_login:active {
  background: #009640;
}

.login-links {
  display: flex;
  align-items: center;
  margin-top: 18px;
  font-size: 13px;
}

.login-links a {
  color: #999;
}

.login-links a:hover {
  color: #00c250;
}

.login-links a:nth-child(2) {
  margin-left: 18px;
}

.login-links__primary {
  margin-left: auto;
  color: #00c250 !important;
}

.login-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0 4px;
}

.login-qr__code {
  width: 180px;
  height: 180px;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 10px;
  margin-bottom: 18px;
}

.qr-grid {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(21, 1fr);
  grid-template-rows: repeat(21, 1fr);
}

.qr-cell {
  background: transparent;
}

.qr-cell.on {
  background: #000;
}

.login-qr__tip {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
}

.login-qr__sub {
  font-size: 12px;
  color: #999;
}

@media (max-width: 820px) {
  .login-panel {
    width: 100%;
    max-width: 360px;
  }
}
```

===FILE: src/components/Captcha.tsx===
```tsx
import './Captcha.css'

type Props = {
  code: string
  onRefresh: () => void
}

export default function Captcha({ code, onRefresh }: Props) {
  const width = 110
  const height = 44
  const colors = ['#333', '#00a847', '#555', '#777']

  return (
    <img
      data-testid="captcha-image"
      className="captcha-image"
      width={width}
      height={height}
      alt="点击刷新验证码"
      title="点击刷新验证码"
      onClick={onRefresh}
      src={buildSvg(code, width, height, colors)}
    />
  )
}

function buildSvg(code: string, w: number, h: number, colors: string[]) {
  const chars = code.split('')
  const letters = chars
    .map((c, i) => {
      const x = 12 + i * 24 + Math.random() * 4
      const y = 30 + (Math.random() * 6 - 3)
      const rot = Math.floor(Math.random() * 30 - 15)
      const color = colors[i % colors.length]
      return `<text x="${x}" y="${y}" fill="${color}" font-size="22" font-family="Arial" font-weight="bold" transform="rotate(${rot} ${x} ${y})">${c}</text>`
    })
    .join('')

  const lines = Array.from({ length: 3 })
    .map(() => {
      const x1 = Math.random() * w
      const y1 = Math.random() * h
      const x2 = Math.random() * w
      const y2 = Math.random() * h
      const color = colors[Math.floor(Math.random() * colors.length)]
      return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="1" opacity="0.4"/>`
    })
    .join('')

  const dots = Array.from({ length: 18 })
    .map(() => {
      const cx = Math.random() * w
      const cy = Math.random() * h
      const color = colors[Math.floor(Math.random() * colors.length)]
      return `<circle cx="${cx}" cy="${cy}" r="1" fill="${color}" opacity="0.5"/>`
    })
    .join('')

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="#f2f2f2"/>${lines}${dots}${letters}</svg>`

  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`
}
```

===FILE: src/components/Captcha.css===
```css
.captcha-image {
  height: 44px;
  width: 110px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  display: block;
  background: #f2f2f2;
  flex-shrink: 0;
}

.captcha-image:hover {
  border-color: #00c250;
}
```

===FILE: src/components/Footer.tsx===
```tsx
import './Footer.css'

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <span>客服热线：95017-2</span>
        <span className="dot">·</span>
        <span>服务时间：09:00-22:00</span>
        <span className="dot">·</span>
        <span>Powered By Tencent &amp; Tenpay</span>
      </div>
      <div className="site-footer__copy">
        Copyright 2005-2026 Tenpay All Rights Reserved.
      </div>
    </footer>
  )
}
```

===FILE: src/components/Footer.css===
```css
.site-footer {
  background: #2d3033;
  color: #9d9d9d;
  padding: 22px 24px;
  text-align: center;
}

.site-footer__inner {
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}

.site-footer__inner .dot {
  color: #555;
}

.site-footer__copy {
  font-size: 12px;
  color: #777;
  margin-top: 10px;
}
```