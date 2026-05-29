===FILE: package.json===
{
  "name": "github-login-clone",
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

===FILE: vite.config.ts===
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})

===FILE: tsconfig.json===
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

===FILE: tsconfig.node.json===
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

===FILE: index.html===
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sign in to GitHub · GitHub</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>

===FILE: src/main.tsx===
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

===FILE: src/index.css===
:root {
  --color-fg-default: rgb(31, 35, 40);
  --color-fg-muted: rgb(89, 99, 110);
  --color-canvas-default: rgb(255, 255, 255);
  --color-canvas-subtle: rgb(246, 248, 250);
  --color-accent-fg: rgb(9, 105, 218);
  --color-success-fg: rgb(31, 136, 61);
  --color-border-default: #d1d9e0;
  --font-stack: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI",
    "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji";
}

* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-stack);
  color: var(--color-fg-default);
  background-color: var(--color-canvas-default);
  font-size: 14px;
  -webkit-font-smoothing: antialiased;
  line-height: 1.5;
}

a {
  color: var(--color-accent-fg);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

===FILE: src/App.tsx===
import { useState } from 'react'
import LoginForm from './components/LoginForm'
import Footer from './components/Footer'
import './App.css'

function App() {
  return (
    <div className="page">
      <main className="login-container">
        <LoginForm />
      </main>
      <Footer />
    </div>
  )
}

export default App

===FILE: src/App.css===
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--color-canvas-default);
}

.login-container {
  flex: 1;
  width: 340px;
  max-width: calc(100% - 32px);
  margin: 0 auto;
  padding: 40px 0 0;
}

===FILE: src/components/LoginForm.tsx===
import { useState, FormEvent } from 'react'

function GitHubMark() {
  return (
    <svg
      height="48"
      width="48"
      viewBox="0 0 16 16"
      aria-hidden="true"
      className="github-mark"
    >
      <path
        fill="currentColor"
        d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.075-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"
      />
    </svg>
  )
}

function LoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setSubmitted(true)
    // Mock login flow: validate non-empty fields then "submit"
    if (username.trim() && password.trim()) {
      window.alert(`Signing in as ${username}`)
    }
  }

  return (
    <div className="login">
      <div className="login-logo">
        <GitHubMark />
      </div>
      <h1 className="login-title">Sign in to GitHub</h1>

      <div className="auth-form">
        <form onSubmit={handleSubmit} noValidate={false}>
          <div className="form-group">
            <label htmlFor="login_field">Username or email address</label>
            <input
              id="login_field"
              name="login"
              type="text"
              className="form-control"
              autoComplete="username"
              autoCapitalize="off"
              autoCorrect="off"
              spellCheck={false}
              autoFocus
              required
              data-testid="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="form-group">
            <div className="password-label-row">
              <label htmlFor="password">Password</label>
              <a
                href="#"
                className="forgot-link"
                data-testid="forgot-password"
                onClick={(e) => e.preventDefault()}
              >
                Forgot password?
              </a>
            </div>
            <input
              id="password"
              name="password"
              type="password"
              className="form-control"
              autoComplete="current-password"
              required
              data-testid="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <input
            type="submit"
            name="commit"
            className="btn btn-primary btn-block"
            value="Sign in"
            data-testid="submit-button"
          />
        </form>

        {submitted && (!username.trim() || !password.trim()) && (
          <p className="validation-message" data-testid="validation-message">
            Please fill in all required fields.
          </p>
        )}

        <div className="login-divider">
          <span>or</span>
        </div>

        <button type="button" className="btn btn-block social-btn">
          <svg
            className="social-icon"
            width="18"
            height="18"
            viewBox="0 0 18 18"
            aria-hidden="true"
          >
            <path
              fill="#4285F4"
              d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844a4.14 4.14 0 0 1-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615Z"
            />
            <path
              fill="#34A853"
              d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18Z"
            />
            <path
              fill="#FBBC05"
              d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332Z"
            />
            <path
              fill="#EA4335"
              d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58Z"
            />
          </svg>
          Continue with Google
        </button>

        <button type="button" className="btn btn-block social-btn">
          <svg
            className="social-icon"
            width="16"
            height="18"
            viewBox="0 0 16 18"
            aria-hidden="true"
          >
            <path
              fill="#000000"
              d="M13.07 9.5c-.02-1.97 1.61-2.92 1.68-2.97-.92-1.34-2.34-1.52-2.85-1.54-1.21-.12-2.37.71-2.99.71-.61 0-1.57-.69-2.58-.67-1.33.02-2.55.77-3.23 1.96-1.38 2.39-.35 5.93 1 7.87.66.95 1.44 2.02 2.47 1.98.99-.04 1.36-.64 2.56-.64 1.19 0 1.53.64 2.57.62 1.06-.02 1.74-.97 2.39-1.92.75-1.1 1.06-2.17 1.08-2.22-.02-.01-2.07-.79-2.09-3.15ZM11.1 3.21c.55-.66.92-1.59.82-2.51-.79.03-1.75.53-2.31 1.19-.5.58-.94 1.52-.82 2.42.88.07 1.78-.45 2.31-1.1Z"
            />
          </svg>
          Continue with Apple
        </button>

        <div className="create-account">
          New to GitHub?{' '}
          <a
            href="https://github.com/signup"
            data-testid="signup-link"
          >
            Create an account
          </a>
        </div>

        <div className="passkey-row">
          <a href="#" className="passkey-link" onClick={(e) => e.preventDefault()}>
            Sign in with a passkey
          </a>
        </div>
      </div>
    </div>
  )
}

export default LoginForm

===FILE: src/components/LoginForm.css===
/* styles live in App.css scope via index import; kept for clarity */

===FILE: src/components/Footer.tsx===
function Footer() {
  const links = [
    { label: 'Terms', href: '#' },
    { label: 'Privacy', href: '#' },
    { label: 'Docs', href: '#' },
    { label: 'Contact GitHub Support', href: '#' },
    { label: 'Manage cookies', href: '#' },
    { label: 'Do not share my personal information', href: '#' },
  ]

  return (
    <footer className="site-footer">
      <ul className="footer-links">
        {links.map((link) => (
          <li key={link.label}>
            <a href={link.href} onClick={(e) => e.preventDefault()}>
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </footer>
  )
}

export default Footer

===FILE: src/components/styles.css===
.login {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-logo {
  color: var(--color-fg-default);
  margin-bottom: 16px;
}

.github-mark {
  display: block;
}

.login-title {
  font-size: 24px;
  font-weight: 300;
  letter-spacing: -0.5px;
  text-align: center;
  margin: 0 0 16px;
  color: var(--color-fg-default);
}

.auth-form {
  width: 100%;
}

.form-group {
  margin-bottom: 16px;
  text-align: left;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--color-fg-default);
}

.password-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.password-label-row label {
  margin-bottom: 0;
}

.forgot-link {
  font-size: 12px;
}

.form-control {
  width: 100%;
  height: 33px;
  padding: 5px 12px;
  font-size: 14px;
  line-height: 20px;
  color: var(--color-fg-default);
  background-color: var(--color-canvas-default);
  border: 1px solid var(--color-border-default);
  border-radius: 6px;
  outline: none;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: var(--color-accent-fg);
  box-shadow: 0 0 0 1px var(--color-accent-fg);
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 32px;
  padding: 5px 16px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid transparent;
  font-family: inherit;
}

.btn-block {
  width: 100%;
}

.btn-primary {
  color: #ffffff;
  background-color: var(--color-success-fg);
  border-color: rgba(31, 35, 40, 0.15);
  font-size: 14px;
  font-weight: 600;
  height: 36px;
}

.btn-primary:hover {
  background-color: rgb(26, 116, 51);
}

.btn-primary:active {
  background-color: rgb(22, 102, 45);
}

.social-btn {
  margin-top: 10px;
  color: var(--color-fg-default);
  background-color: var(--color-canvas-subtle);
  border-color: var(--color-border-default);
  font-weight: 500;
}

.social-btn:hover {
  background-color: #eef1f4;
}

.social-icon {
  flex-shrink: 0;
}

.validation-message {
  color: #cf222e;
  font-size: 12px;
  margin: -8px 0 12px;
  text-align: left;
}

.login-divider {
  position: relative;
  text-align: center;
  margin: 16px 0;
  color: var(--color-fg-default);
  font-size: 14px;
}

.login-divider::before,
.login-divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: calc(50% - 20px);
  height: 1px;
  background-color: var(--color-border-default);
}

.login-divider::before {
  left: 0;
}

.login-divider::after {
  right: 0;
}

.login-divider span {
  position: relative;
  padding: 0 8px;
  background-color: var(--color-canvas-default);
}

.create-account {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: var(--color-fg-default);
}

.passkey-row {
  text-align: center;
  margin-top: 16px;
}

.passkey-link {
  font-size: 14px;
  font-weight: 600;
}

.site-footer {
  margin-top: auto;
  padding: 24px 16px;
  background-color: var(--color-canvas-subtle);
  border-top: 1px solid var(--color-border-default);
}

.footer-links {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 8px 16px;
  margin: 0;
  padding: 0;
  max-width: 1012px;
  margin-inline: auto;
}

.footer-links a {
  font-size: 12px;
  color: var(--color-accent-fg);
}

.footer-links li {
  display: flex;
}

@media (max-width: 544px) {
  .footer-links {
    flex-direction: column;
    gap: 8px;
  }
}