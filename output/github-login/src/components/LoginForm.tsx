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
