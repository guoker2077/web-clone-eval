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
