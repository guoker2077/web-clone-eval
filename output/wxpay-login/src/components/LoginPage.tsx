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
