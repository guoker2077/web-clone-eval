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
    "typescript": "^5.5.4",
    "vite": "^5.4.2"
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
    <title>微信支付商户平台-登录</title>
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
body,
#root {
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

:root {
  --green: #00c250;
  --green-dark: #00a847;
  --text-main: #333;
  --text-sub: #9d9d9d;
  --border: #e8e8e8;
}
```

===FILE: src/App.tsx===
```tsx
import LoginPage from './components/LoginPage'

export default function App() {
  return <LoginPage />
}
```

===FILE: src/components/LoginPage.tsx===
```tsx
import { useState } from 'react'
import LoginForm from './LoginForm'
import './LoginPage.css'

const NAV = ['首页', '产品中心', '服务中心', '帮助中心', '商家故事']

export default function LoginPage() {
  const [activeNav] = useState(0)

  return (
    <div className="page">
      {/* Top utility bar */}
      <div className="topbar">
        <div className="topbar-inner">
          <span className="topbar-active">微信支付</span>
          <span className="topbar-divider">|</span>
          <span>商户平台</span>
          <span className="topbar-divider">|</span>
          <span className="topbar-intl">International Business</span>
        </div>
      </div>

      {/* Header */}
      <header className="header">
        <div className="header-inner">
          <div className="brand">
            <span className="brand-logo">
              <svg viewBox="0 0 48 48" width="36" height="36" aria-hidden>
                <circle cx="24" cy="24" r="24" fill="#00c250" />
                <path
                  d="M14 26.5l5.5 5 13-13"
                  fill="none"
                  stroke="#fff"
                  strokeWidth="3.4"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </span>
            <span className="brand-name">微信支付</span>
          </div>

          <nav className="nav">
            {NAV.map((item, i) => (
              <a
                key={item}
                className={`nav-item ${i === activeNav ? 'active' : ''}`}
                href="#"
                onClick={(e) => e.preventDefault()}
              >
                {item}
              </a>
            ))}
          </nav>

          <button
            className="btn-register"
            onClick={(e) => e.preventDefault()}
          >
            商户接入指引
          </button>
        </div>
      </header>

      {/* Main: hero + login card */}
      <main className="hero">
        <div className="hero-inner">
          <div className="hero-copy">
            <h1 className="hero-title">微信支付商户平台</h1>
            <p className="hero-sub">
              连接每个商家与用户，让经营更简单，让收款更安心
            </p>
            <ul className="hero-points">
              <li>安全稳定的资金保障</li>
              <li>丰富完善的支付能力</li>
              <li>智能高效的经营工具</li>
            </ul>
          </div>

          <LoginForm />
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-inner">
          <span>关于微信支付</span>
          <span className="footer-divider">|</span>
          <span>商户接入</span>
          <span className="footer-divider">|</span>
          <span>合作伙伴</span>
          <span className="footer-divider">|</span>
          <span>服务条款</span>
        </div>
        <div className="footer-copy">
          Powered By Tencent &amp; Tenpay&nbsp;&nbsp;Copyright 2005-2026 Tenpay
          All Rights Reserved.
        </div>
      </footer>
    </div>
  )
}
```

===FILE: src/components/LoginPage.css===
```css
.page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  background: #fff;
}

/* Top utility bar */
.topbar {
  background: #2e2e2e;
  color: #c8c8c8;
  font-size: 12px;
  height: 32px;
}
.topbar-inner {
  max-width: 1100px;
  margin: 0 auto;
  height: 32px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 12px;
}
.topbar-active {
  color: #00c250;
}
.topbar-divider {
  color: #555;
}
.topbar-intl {
  color: #fff;
}

/* Header */
.header {
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
}
.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 20px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-logo {
  display: inline-flex;
}
.brand-name {
  font-size: 20px;
  font-weight: 500;
  color: #000;
}
.nav {
  display: flex;
  align-items: center;
  gap: 38px;
  margin-left: auto;
}
.nav-item {
  font-size: 14px;
  color: #333;
  position: relative;
  padding: 6px 0;
}
.nav-item:hover {
  color: #00c250;
}
.nav-item.active {
  color: #00c250;
}
.nav-item.active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -6px;
  height: 2px;
  background: #00c250;
}
.btn-register {
  margin-left: 38px;
  background: #00c250;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  padding: 9px 20px;
  cursor: pointer;
}
.btn-register:hover {
  background: #00a847;
}

/* Hero */
.hero {
  flex: 1;
  background: linear-gradient(135deg, #00c250 0%, #00a847 100%);
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  right: -120px;
  top: -80px;
  width: 460px;
  height: 460px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 50%;
}
.hero::after {
  content: '';
  position: absolute;
  left: -100px;
  bottom: -160px;
  width: 380px;
  height: 380px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
}
.hero-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 70px 20px 90px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
  position: relative;
  z-index: 1;
}
.hero-copy {
  color: #fff;
  max-width: 460px;
}
.hero-title {
  font-size: 36px;
  font-weight: 600;
  margin-bottom: 16px;
}
.hero-sub {
  font-size: 16px;
  line-height: 1.7;
  opacity: 0.92;
  margin-bottom: 28px;
}
.hero-points {
  list-style: none;
  font-size: 14px;
  line-height: 2.2;
}
.hero-points li {
  position: relative;
  padding-left: 22px;
  opacity: 0.95;
}
.hero-points li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
}
.hero-points li::after {
  content: '';
  position: absolute;
  left: 3px;
  top: calc(50% - 2px);
  width: 5px;
  height: 3px;
  border-left: 1.5px solid #fff;
  border-bottom: 1.5px solid #fff;
  transform: rotate(-45deg);
}

/* Footer */
.footer {
  background: #404343;
  color: #999;
  text-align: center;
  padding: 28px 20px;
}
.footer-inner {
  font-size: 13px;
  margin-bottom: 14px;
}
.footer-divider {
  margin: 0 12px;
  color: #5a5d5d;
}
.footer-copy {
  font-size: 12px;
  color: #777;
}

@media (max-width: 820px) {
  .hero-inner {
    flex-direction: column;
    align-items: stretch;
    padding: 40px 20px 60px;
  }
  .hero-copy {
    text-align: center;
    margin: 0 auto;
  }
  .nav {
    display: none;
  }
}
```

===FILE: src/components/LoginForm.tsx===
```tsx
import { useState } from 'react'
import Captcha from './Captcha'
import './LoginForm.css'

type Tab = 'account' | 'qr'

export default function LoginForm() {
  const [tab, setTab] = useState<Tab>('account')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [captcha, setCaptcha] = useState('')
  const [captchaCode, setCaptchaCode] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleLogin = () => {
    setSuccess(false)
    if (!username.trim()) {
      setError('请输入登录账号')
      return
    }
    if (!password.trim()) {
      setError('请输入登录密码')
      return
    }
    if (!captcha.trim()) {
      setError('请输入验证码')
      return
    }
    if (captcha.trim().toLowerCase() !== captchaCode.toLowerCase()) {
      setError('验证码不正确')
      return
    }
    setError('')
    setLoading(true)
    // mock async login
    window.setTimeout(() => {
      setLoading(false)
      setSuccess(true)
    }, 600)
  }

  return (
    <div className="login-card" data-testid="login-card">
      <div className="login-tabs">
        <button
          className={`login-tab ${tab === 'account' ? 'active' : ''}`}
          onClick={() => setTab('account')}
          type="button"
        >
          账号登录
        </button>
        <button
          className={`login-tab ${tab === 'qr' ? 'active' : ''}`}
          onClick={() => setTab('qr')}
          type="button"
        >
          扫码登录
        </button>
      </div>

      {tab === 'account' ? (
        <form
          className="login-body"
          onSubmit={(e) => {
            e.preventDefault()
            handleLogin()
          }}
        >
          <div className="field">
            <input
              id="idUserName"
              name="username"
              data-testid="username"
              className="field-input"
              type="text"
              placeholder="登录账号"
              value={username}
              autoComplete="username"
              onChange={(e) => {
                setUsername(e.target.value)
                setError('')
              }}
            />
          </div>

          <div className="field">
            <input
              id="idPassword"
              name="password"
              data-testid="password"
              className="field-input"
              type="password"
              placeholder="登录密码"
              value={password}
              autoComplete="current-password"
              onChange={(e) => {
                setPassword(e.target.value)
                setError('')
              }}
            />
          </div>

          <div className="field field-captcha">
            <input
              name="checkword_in"
              data-testid="captcha-input"
              className="field-input"
              type="text"
              placeholder="验证码"
              value={captcha}
              maxLength={6}
              onChange={(e) => {
                setCaptcha(e.target.value)
                setError('')
              }}
            />
            <Captcha onChange={setCaptchaCode} />
          </div>

          {error && (
            <div className="login-error" data-testid="login-error">
              {error}
            </div>
          )}
          {success && (
            <div className="login-success" data-testid="login-success">
              登录成功，正在跳转…
            </div>
          )}

          <button
            type="submit"
            className="btn-login login"
            data-testid="login-button"
            disabled={loading}
          >
            {loading ? '登录中…' : '登 录'}
          </button>

          <div className="login-links">
            <a href="#" onClick={(e) => e.preventDefault()}>
              忘记密码
            </a>
            <a href="#" onClick={(e) => e.preventDefault()}>
              注册账号
            </a>
          </div>
        </form>
      ) : (
        <div className="login-body qr-body">
          <div className="qr-box">
            <div className="qr-img" aria-hidden>
              {Array.from({ length: 144 }).map((_, i) => (
                <span
                  key={i}
                  style={{
                    background: (i * 7 + (i % 5)) % 3 === 0 ? '#222' : 'transparent',
                  }}
                />
              ))}
            </div>
          </div>
          <p className="qr-tip">请使用微信扫一扫登录</p>
        </div>
      )}
    </div>
  )
}
```

===FILE: src/components/LoginForm.css===
```css
.login-card {
  width: 360px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  flex-shrink: 0;
}

.login-tabs {
  display: flex;
  border-bottom: 1px solid #e8e8e8;
}
.login-tab {
  flex: 1;
  background: #f7f6f2;
  border: none;
  font-size: 16px;
  color: #999;
  padding: 16px 0;
  cursor: pointer;
  position: relative;
}
.login-tab.active {
  background: #fff;
  color: #333;
  font-weight: 500;
}
.login-tab.active::after {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 0;
  width: 48px;
  height: 2px;
  background: #00c250;
}

.login-body {
  padding: 30px 32px 28px;
  display: flex;
  flex-direction: column;
}

.field {
  margin-bottom: 18px;
}
.field-input {
  width: 100%;
  height: 44px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 0 14px;
  font-size: 14px;
  color: #333;
  outline: none;
  transition: border-color 0.15s;
}
.field-input::placeholder {
  color: #b5b5b5;
}
.field-input:focus {
  border-color: #00c250;
}

.field-captcha {
  display: flex;
  align-items: center;
  gap: 10px;
}
.field-captcha .field-input {
  flex: 1;
}

.login-error {
  color: #e34d59;
  font-size: 13px;
  margin: -4px 0 14px;
}
.login-success {
  color: #00c250;
  font-size: 13px;
  margin: -4px 0 14px;
}

.btn-login {
  width: 100%;
  height: 46px;
  background: #00c250;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  letter-spacing: 4px;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-login:hover {
  background: #00a847;
}
.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-links {
  display: flex;
  justify-content: space-between;
  margin-top: 18px;
  font-size: 13px;
}
.login-links a {
  color: #9d9d9d;
}
.login-links a:hover {
  color: #00c250;
}

/* QR tab */
.qr-body {
  align-items: center;
  padding-top: 24px;
}
.qr-box {
  padding: 12px;
  border: 1px solid #eee;
  border-radius: 6px;
}
.qr-img {
  width: 168px;
  height: 168px;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: repeat(12, 1fr);
}
.qr-img span {
  display: block;
}
.qr-tip {
  margin-top: 16px;
  font-size: 13px;
  color: #9d9d9d;
}
```

===FILE: src/components/Captcha.tsx===
```tsx
import { useCallback, useEffect, useRef, useState } from 'react'
import './Captcha.css'

const CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'

function randomCode(len = 4): string {
  let s = ''
  for (let i = 0; i < len; i++) {
    s += CHARS[Math.floor(Math.random() * CHARS.length)]
  }
  return s
}

interface Props {
  onChange: (code: string) => void
}

export default function Captcha({ onChange }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [code, setCode] = useState('')

  const draw = useCallback(
    (value: string) => {
      const canvas = canvasRef.current
      if (!canvas) return
      const ctx = canvas.getContext('2d')
      if (!ctx) return

      const w = canvas.width
      const h = canvas.height
      ctx.clearRect(0, 0, w, h)
      ctx.fillStyle = '#f2f4f7'
      ctx.fillRect(0, 0, w, h)

      // interference lines
      for (let i = 0; i < 4; i++) {
        ctx.strokeStyle = `rgba(${rnd(120, 200)},${rnd(120, 200)},${rnd(
          120,
          200
        )},0.6)`
        ctx.beginPath()
        ctx.moveTo(rnd(0, w), rnd(0, h))
        ctx.lineTo(rnd(0, w), rnd(0, h))
        ctx.stroke()
      }

      // characters
      const colors = ['#00a847', '#3b7fd4', '#e3852b', '#7a52c9', '#d0455a']
      for (let i = 0; i < value.length; i++) {
        ctx.save()
        const x = 12 + i * 22
        const y = h / 2 + rnd(-3, 3)
        ctx.translate(x, y)
        ctx.rotate(((rnd(-22, 22) * Math.PI) / 180))
        ctx.font = `bold ${rnd(22, 26)}px Arial`
        ctx.fillStyle = colors[i % colors.length]
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(value[i], 0, 0)
        ctx.restore()
      }

      // dots
      for (let i = 0; i < 18; i++) {
        ctx.fillStyle = `rgba(${rnd(100, 200)},${rnd(100, 200)},${rnd(
          100,
          200
        )},0.7)`
        ctx.beginPath()
        ctx.arc(rnd(0, w), rnd(0, h), 1, 0, Math.PI * 2)
        ctx.fill()
      }
    },
    []
  )

  const refresh = useCallback(() => {
    const next = randomCode()
    setCode(next)
    onChange(next)
    draw(next)
  }, [draw, onChange])

  useEffect(() => {
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <canvas
      ref={canvasRef}
      width={100}
      height={44}
      className="captcha-canvas"
      data-testid="captcha-image"
      title="点击刷新验证码"
      onClick={refresh}
      role="img"
      aria-label={`验证码 ${code}`}
    />
  )
}

function rnd(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}
```

===FILE: src/components/Captcha.css===
```css
.captcha-canvas {
  width: 100px;
  height: 44px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  display: block;
  flex-shrink: 0;
}
.captcha-canvas:hover {
  border-color: #00c250;
}
```