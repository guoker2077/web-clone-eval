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
