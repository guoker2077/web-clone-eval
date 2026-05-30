===FILE: package.json===
{
  "name": "github-login-clone",
  "private": true,
  "version": "0.0.0",
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
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "typescript": "^5.5.3",
    "vite": "^5.3.4"
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
import App from './App'
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
  --color-border-default: #d1d9e0;
  --color-btn-primary-bg: rgb(31, 136, 61);
  --color-btn-primary-hover: rgb(26, 119, 53);
  --color-input-border: #d1d9e0;
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
  font-family: "Mona Sans VF", -apple-system, BlinkMacSystemFont, "Segoe UI",
    "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji";
  font-size: 14px;
  line-height: 1.5;
  color: var(--color-fg-default);
  background-color: var(--color-canvas-default);
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--color-accent-fg);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

===FILE: src/App.tsx===
import LoginForm from './components/LoginForm'
import Footer from './components/Footer'
import './App.css'

function App() {
  return (
    <div className="app">
      <main className="login-container">
        <LoginForm />
      </main>
      <Footer />
    </div>
  )
}

export default App

===FILE: src/App.css===
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--color-canvas-default);
}

.login-container {
  flex: 1 0 auto;
  width: 308px;
  max-width: 100%;
  margin: 0 auto;
  padding: 40px 16px 0;
}

===FILE: src/components/LoginForm.tsx===
import { useState } from 'react'
import GitHubMark from './GitHubMark'
import './LoginForm.css'

function LoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    // HTML5 required validation is handled by the form fields.
    // On valid submission we simply mark the state as submitted (mock flow).
    setSubmitted(true)
  }

  return (
    <div className="login-form">
      <div className="login-form__logo">
        <GitHubMark />
      </div>

      <h1 className="login-form__title">Sign in to GitHub</h1>

      <div className="login-form__box">
        <form onSubmit={handleSubmit} noValidate={false}>
          <div className="form-group">
            <label htmlFor="login_field">Username or email address</label>
            <input
              id="login_field"
              name="login"
              type="text"
              className="form-control"
              data-testid="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              autoCapitalize="none"
              autoCorrect="off"
              required
            />
          </div>

          <div className="form-group">
            <div className="form-group__password-header">
              <label htmlFor="password">Password</label>
              <a className="form-group__forgot" href="#forgot">
                Forgot password?
              </a>
            </div>
            <input
              id="password"
              name="password"
              type="password"
              className="form-control"
              data-testid="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>

          <input
            type="submit"
            name="commit"
            value="Sign in"
            className="btn btn-primary"
            data-testid="submit-button"
          />
        </form>

        {submitted && (
          <p className="login-form__status" role="status">
            Signed in as {username} (mock).
          </p>
        )}
      </div>

      <div className="login-form__divider">
        <span className="login-form__divider-line" />
        <span className="login-form__divider-text">or</span>
        <span className="login-form__divider-line" />
      </div>

      <button type="button" className="btn btn-social">
        <span className="btn-social__icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 18 18">
            <path
              fill="#4285F4"
              d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844a4.14 4.14 0 0 1-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615z"
            />
            <path
              fill="#34A853"
              d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z"
            />
            <path
              fill="#FBBC05"
              d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z"
            />
            <path
              fill="#EA4335"
              d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"
            />
          </svg>
        </span>
        Continue with Google
      </button>

      <button type="button" className="btn btn-social">
        <span className="btn-social__icon" aria-hidden="true">
          <svg width="16" height="18" viewBox="0 0 14 16" fill="#000">
            <path d="M11.182.008C11.148-.03 9.923.023 8.857 1.18c-1.066 1.156-.902 2.482-.878 2.516.024.034 1.52.087 2.475-1.258.955-1.345.762-2.391.728-2.43zm3.314 11.733c-.048-.096-2.325-1.234-2.113-3.422.212-2.189 1.675-2.789 1.698-2.854.023-.065-.597-.79-1.254-1.157a3.692 3.692 0 0 0-1.563-.434c-.108-.003-.483-.095-1.254.116-.508.139-1.653.589-1.968.607-.316.018-1.256-.522-2.267-.665-.647-.125-1.333.131-1.824.328-.49.196-1.422.754-2.074 2.237-.652 1.482-.311 3.83-.067 4.56.244.729.625 1.924 1.273 2.796.576.984 1.34 1.667 1.659 1.899.319.232 1.219.386 1.843.067.502-.308 1.408-.485 1.766-.472.357.013 1.061.154 1.782.539.571.197 1.111.115 1.652-.105.541-.221 1.324-1.059 2.238-2.758.347-.79.505-1.217.473-1.282z" />
          </svg>
        </span>
        Continue with Apple
      </button>

      <div className="login-form__signup">
        New to GitHub?{' '}
        <a href="https://github.com/signup" data-testid="signup-link">
          Create an account
        </a>
      </div>

      <div className="login-form__passkey">
        <a href="#passkey">Sign in with a passkey</a>
      </div>
    </div>
  )
}

export default LoginForm

===FILE: src/components/LoginForm.css===
.login-form {
  display: flex;
  flex-direction: column;
}

.login-form__logo {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.login-form__logo svg {
  fill: var(--color-fg-default);
}

.login-form__title {
  font-size: 20px;
  font-weight: 300;
  line-height: 1.25;
  text-align: center;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
}

.login-form__box {
  margin-top: 4px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--color-fg-default);
}

.form-group__password-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-group__password-header label {
  margin-bottom: 8px;
}

.form-group__forgot {
  font-size: 12px;
}

.form-control {
  display: block;
  width: 100%;
  height: 32px;
  padding: 5px 12px;
  font-size: 14px;
  line-height: 20px;
  color: var(--color-fg-default);
  background-color: var(--color-canvas-default);
  border: 1px solid var(--color-input-border);
  border-radius: 6px;
  outline: none;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: var(--color-accent-fg);
  box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.3);
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 32px;
  padding: 5px 16px;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  border-radius: 6px;
  border: 1px solid transparent;
  cursor: pointer;
  appearance: none;
  user-select: none;
}

.btn-primary {
  color: #ffffff;
  background-color: var(--color-btn-primary-bg);
  border-color: rgba(31, 35, 40, 0.15);
  margin-top: 16px;
}

.btn-primary:hover {
  background-color: var(--color-btn-primary-hover);
}

.btn-social {
  color: var(--color-fg-default);
  background-color: var(--color-canvas-default);
  border: 1px solid var(--color-border-default);
  margin-bottom: 12px;
  font-weight: 500;
}

.btn-social:hover {
  background-color: var(--color-canvas-subtle);
}

.btn-social__icon {
  display: inline-flex;
  align-items: center;
  margin-right: 8px;
}

.login-form__status {
  margin: 12px 0 0;
  font-size: 13px;
  color: var(--color-btn-primary-bg);
}

.login-form__divider {
  display: flex;
  align-items: center;
  margin: 16px 0;
  color: var(--color-fg-muted);
  font-size: 14px;
}

.login-form__divider-line {
  flex: 1;
  height: 1px;
  background-color: var(--color-border-default);
}

.login-form__divider-text {
  padding: 0 16px;
}

.login-form__signup {
  text-align: center;
  font-size: 14px;
  color: var(--color-fg-default);
  margin-top: 16px;
}

.login-form__passkey {
  text-align: center;
  font-size: 14px;
  margin-top: 16px;
}

===FILE: src/components/GitHubMark.tsx===
function GitHubMark() {
  return (
    <svg height="48" width="48" viewBox="0 0 16 16" aria-hidden="true">
      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z" />
    </svg>
  )
}

export default GitHubMark

===FILE: src/components/Footer.tsx===
import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <nav className="footer__nav" aria-label="Footer">
        <a href="https://docs.github.com/site-policy/github-terms/github-terms-of-service">
          Terms
        </a>
        <a href="https://docs.github.com/site-policy/privacy-policies/github-privacy-statement">
          Privacy
        </a>
        <a href="https://docs.github.com">Docs</a>
        <a href="https://support.github.com">Contact GitHub Support</a>
        <button type="button" className="footer__link-btn">
          Manage cookies
        </button>
        <button type="button" className="footer__link-btn">
          Do not share my personal information
        </button>
      </nav>
    </footer>
  )
}

export default Footer

===FILE: src/components/Footer.css===
.footer {
  flex-shrink: 0;
  width: 100%;
  padding: 24px 16px;
  background-color: var(--color-canvas-subtle);
  border-top: 1px solid var(--color-border-default);
  margin-top: 48px;
}

.footer__nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 16px;
  max-width: 1012px;
  margin: 0 auto;
}

.footer__nav a,
.footer__link-btn {
  font-size: 12px;
  color: var(--color-fg-muted);
}

.footer__nav a:hover,
.footer__link-btn:hover {
  color: var(--color-accent-fg);
  text-decoration: underline;
}

.footer__link-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  font-family: inherit;
}