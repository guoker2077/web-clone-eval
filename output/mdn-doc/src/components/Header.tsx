import { useState } from 'react'
import '../styles/header.css'

export default function Header() {
  const [openMenu, setOpenMenu] = useState<string | null>(null)

  const toggle = (name: string) =>
    setOpenMenu((prev) => (prev === name ? null : name))

  return (
    <header className="site-header" data-testid="header">
      <div className="header-inner">
        <a className="logo" href="/en-US/" data-testid="logo-home" aria-label="MDN homepage">
          <span className="logo-text">mdn</span>
          <span className="logo-underscore">_</span>
        </a>

        <nav className="main-nav" aria-label="Main menu">
          <div className="nav-item">
            <button
              type="button"
              className={`nav-button ${openMenu === 'references' ? 'active' : ''}`}
              aria-expanded={openMenu === 'references'}
              onClick={() => toggle('references')}
            >
              References <span className="chevron">▾</span>
            </button>
          </div>
          <div className="nav-item">
            <button
              type="button"
              className={`nav-button ${openMenu === 'guides' ? 'active' : ''}`}
              aria-expanded={openMenu === 'guides'}
              onClick={() => toggle('guides')}
            >
              Guides <span className="chevron">▾</span>
            </button>
          </div>
          <div className="nav-item">
            <button
              type="button"
              className={`nav-button ${openMenu === 'html' ? 'active' : ''}`}
              aria-expanded={openMenu === 'html'}
              onClick={() => toggle('html')}
              data-testid="nav-html-menu"
            >
              HTML <span className="chevron">▾</span>
            </button>
            {openMenu === 'html' && (
              <div className="nav-dropdown" role="menu">
                <a href="/en-US/docs/Web/HTML/Reference">HTML reference</a>
                <a href="/en-US/docs/Web/HTML/Element">HTML elements</a>
                <a href="/en-US/docs/Web/HTML/Global_attributes">Global attributes</a>
              </div>
            )}
          </div>
          <div className="nav-item">
            <button
              type="button"
              className={`nav-button ${openMenu === 'learn' ? 'active' : ''}`}
              aria-expanded={openMenu === 'learn'}
              onClick={() => toggle('learn')}
              data-testid="nav-learn-menu"
            >
              Learn <span className="chevron">▾</span>
            </button>
            {openMenu === 'learn' && (
              <div className="nav-dropdown" role="menu">
                <a href="/en-US/docs/Learn_web_development">Web development</a>
                <a href="/en-US/docs/Learn_web_development/Getting_started">Getting started</a>
                <a href="/en-US/docs/Learn_web_development/Core">Core modules</a>
              </div>
            )}
          </div>
          <div className="nav-item">
            <a className="nav-button" href="/en-US/blog/" data-testid="nav-blog">
              Blog
            </a>
          </div>
        </nav>

        <div className="header-right">
          <form className="header-search" role="search" onSubmit={(e) => e.preventDefault()}>
            <input
              type="search"
              placeholder="Search MDN"
              aria-label="Search MDN"
              className="search-input"
            />
          </form>
          <button type="button" className="theme-button" aria-label="Theme">
            Theme
          </button>
          <button type="button" className="lang-button">
            English (US)
          </button>
        </div>
      </div>
    </header>
  )
}
