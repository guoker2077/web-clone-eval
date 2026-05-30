import { useState } from 'react'
import type { FormEvent } from 'react'
import './LoginForm.css'

function LoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    // Empty validation: HTML required attributes handle browser-native
    // validation. This guard keeps the form visible and unsubmitted.
    if (!username.trim() || !password.trim()) {
      setMessage('')
      return
    }

    // Mock successful login flow.
    setMessage(`Signed in as ${username}`)
  }

  return (
    <form className="login-form" onSubmit={handleSubmit} noValidate>
      <div className="field">
        <label className="field-label" htmlFor="login_field">
          Username or email address
        </label>
        <input
          id="login_field"
          name="login"
          type="text"
          className="form-input"
          autoComplete="username"
          autoCapitalize="off"
          autoCorrect="off"
          spellCheck={false}
          required
          data-testid="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <div className="field">
        <div className="password-label-row">
          <label className="field-label" htmlFor="password">
            Password
          </label>
          <a href="#" className="forgot-link">
            Forgot password?
          </a>
        </div>
        <input
          id="password"
          name="password"
          type="password"
          className="form-input"
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
        value="Sign in"
        className="submit-button"
        data-testid="submit-button"
      />

      {message && (
        <p className="success-message" data-testid="login-message">
          {message}
        </p>
      )}
    </form>
  )
}

export default LoginForm
