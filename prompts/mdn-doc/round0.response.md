===FILE: package.json===
{
  "name": "mdn-anchor-clone",
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
<html lang="en-US">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
      rel="stylesheet"
    />
    <title>&lt;a&gt;: The Anchor element - HTML | MDN</title>
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
import './styles/global.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

===FILE: src/App.tsx===
import Header from './components/Header'
import Breadcrumb from './components/Breadcrumb'
import LeftSidebar from './components/LeftSidebar'
import Content from './components/Content'
import TableOfContents from './components/TableOfContents'
import './styles/app.css'

export default function App() {
  return (
    <>
      <a className="skip-link" href="#content" data-testid="skip-to-content">
        Skip to main content
      </a>
      <Header />
      <div className="page">
        <LeftSidebar />
        <main className="main-area" id="content">
          <article className="article">
            <Breadcrumb />
            <Content />
          </article>
          <TableOfContents />
        </main>
      </div>
    </>
  )
}

===FILE: src/components/Header.tsx===
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

===FILE: src/components/Breadcrumb.tsx===
import '../styles/breadcrumb.css'

export default function Breadcrumb() {
  return (
    <nav className="breadcrumb" aria-label="Breadcrumb">
      <ol className="breadcrumb-list">
        <li>
          <a href="/en-US/docs/Web" data-testid="breadcrumb-web">
            Web
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a href="/en-US/docs/Web/HTML" data-testid="breadcrumb-html">
            HTML
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a href="/en-US/docs/Web/HTML/Reference" data-testid="breadcrumb-reference">
            Reference
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a
            href="/en-US/docs/Web/HTML/Reference/Elements"
            data-testid="breadcrumb-elements"
          >
            Elements
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a
            className="current"
            aria-current="page"
            href="/en-US/docs/Web/HTML/Reference/Elements/a"
            data-testid="breadcrumb-anchor"
          >
            &lt;a&gt;
          </a>
        </li>
      </ol>
    </nav>
  )
}

===FILE: src/components/LeftSidebar.tsx===
import { useState } from 'react'
import '../styles/sidebar.css'

const elements = [
  '<a>',
  '<abbr>',
  '<acronym>',
  '<address>',
  '<area>',
  '<article>',
  '<aside>',
  '<audio>',
  '<b>',
  '<base>',
  '<bdi>',
  '<bdo>',
]

export default function LeftSidebar() {
  const [filter, setFilter] = useState('')

  const shown = elements.filter((e) =>
    e.toLowerCase().includes(filter.toLowerCase()),
  )

  return (
    <aside className="left-sidebar" aria-label="Related Topics">
      <div className="sidebar-filter">
        <input
          type="text"
          className="filter-input"
          placeholder="Filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          aria-label="Filter sidebar"
        />
        <button type="button" className="add-button">
          + Add JavaScript
        </button>
      </div>

      <nav className="sidebar-nav">
        <h2 className="sidebar-heading">Reference</h2>
        <details open className="sidebar-group">
          <summary>Elements</summary>
          <ul className="sidebar-list">
            {shown.map((el) => (
              <li key={el}>
                <a
                  className={el === '<a>' ? 'sidebar-link active' : 'sidebar-link'}
                  href={`/en-US/docs/Web/HTML/Reference/Elements/${el.replace(/[<>]/g, '')}`}
                >
                  {el}
                </a>
              </li>
            ))}
          </ul>
        </details>
      </nav>
    </aside>
  )
}

===FILE: src/components/TableOfContents.tsx===
import '../styles/toc.css'

const items = [
  { id: 'try_it', label: 'Try it', testid: 'toc-try-it' },
  { id: 'attributes', label: 'Attributes', testid: 'toc-attributes' },
  { id: 'accessibility', label: 'Accessibility', testid: 'toc-accessibility' },
  { id: 'examples', label: 'Examples', testid: 'toc-examples' },
  {
    id: 'security_and_privacy',
    label: 'Security and privacy',
    testid: 'toc-security-privacy',
  },
  {
    id: 'technical_summary',
    label: 'Technical summary',
    testid: 'toc-technical-summary',
  },
  { id: 'specifications', label: 'Specifications', testid: 'toc-specifications' },
  {
    id: 'browser_compatibility',
    label: 'Browser compatibility',
    testid: 'toc-browser-compatibility',
  },
  { id: 'see_also', label: 'See also', testid: 'toc-see-also' },
]

export default function TableOfContents() {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault()
    const target = document.getElementById(id)
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      history.replaceState(null, '', `#${id}`)
    }
  }

  return (
    <aside className="toc" aria-label="In this article">
      <div className="toc-sticky">
        <h2 className="toc-title">In this article</h2>
        <ul className="toc-list" data-testid="toc-list">
          {items.map((item) => (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                data-testid={item.testid}
                onClick={(e) => handleClick(e, item.id)}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  )
}

===FILE: src/components/Content.tsx===
import '../styles/content.css'

export default function Content() {
  return (
    <>
      <h1 className="page-title">
        <code>&lt;a&gt;</code>: The Anchor element
      </h1>

      <div className="baseline-box">
        <span className="baseline-check">✓</span>
        <span className="baseline-text">
          <strong>Baseline</strong> Widely available
        </span>
      </div>

      <p>
        The <code>&lt;a&gt;</code>{' '}
        <a href="/en-US/docs/Web/HTML">HTML</a> element (or <em>anchor</em>{' '}
        element), with{' '}
        <a href="/en-US/docs/Web/HTML/Reference/Elements/a#href">its <code>href</code> attribute</a>,
        creates a hyperlink to web pages, files, email addresses, locations in
        the same page, or anything else a URL can address.
      </p>

      <p>
        Content within each <code>&lt;a&gt;</code> <em>should</em> indicate the
        link's destination. If the <code>href</code> attribute is present,
        pressing the enter key while focused on the <code>&lt;a&gt;</code> element
        will activate it.
      </p>

      <section id="try_it" className="content-section">
        <h2 className="section-heading">Try it</h2>
        <div className="demo-box">
          <div className="demo-tabs">
            <button type="button" className="demo-tab active">
              HTML
            </button>
            <button type="button" className="demo-tab">
              CSS
            </button>
            <button type="button" className="demo-reset">
              Reset
            </button>
          </div>
          <div className="demo-body">
            <pre className="demo-code">
{`<p>You can reach Michael at:</p>

<ul>
  <li><a href="https://example.com">Website</a></li>
  <li><a href="mailto:m.bluth@example.com">Email</a></li>
  <li><a href="tel:+123456789">Phone</a></li>
</ul>`}
            </pre>
            <div className="demo-output">
              <p>You can reach Michael at:</p>
              <ul>
                <li>
                  <a href="https://example.com">Website</a>
                </li>
                <li>
                  <a href="mailto:m.bluth@example.com">Email</a>
                </li>
                <li>
                  <a href="tel:+123456789">Phone</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section id="attributes" className="content-section">
        <h2 className="section-heading">Attributes</h2>
        <p>
          This element's attributes include the{' '}
          <a
            href="/en-US/docs/Web/HTML/Reference/Global_attributes"
            data-testid="content-global-attributes"
          >
            global attributes
          </a>
          .
        </p>

        <dl className="attr-list">
          <dt id="attributionsrc">
            <a href="#attributionsrc">
              <code>attributionsrc</code>
            </a>{' '}
            <span className="badge experimental">Experimental</span>
          </dt>
          <dd>
            Specifies that you want the browser to send an{' '}
            <code>Attribution-Reporting-Eligible</code> header. On the
            server-side this is used to trigger sending an{' '}
            <code>Attribution-Reporting-Register-Source</code> header in the
            response, to register a navigation-based attribution source.
          </dd>

          <dt id="download">
            <a href="#download" data-testid="content-attr-download">
              <code>download</code>
            </a>
          </dt>
          <dd>
            Causes the browser to treat the linked URL as a download. Can be used
            with or without a <code>filename</code> value.
          </dd>

          <dt id="href">
            <a href="#href">
              <code>href</code>
            </a>
          </dt>
          <dd>
            The URL that the hyperlink points to. Links are not restricted to
            HTTP-based URLs — they can use any URL scheme supported by browsers.
          </dd>

          <dt id="hreflang">
            <a href="#hreflang" data-testid="content-attr-hreflang">
              <code>hreflang</code>
            </a>
          </dt>
          <dd>
            Hints at the human language of the linked URL. No built-in
            functionality. Allowed values are the same as the{' '}
            <code>lang</code> global attribute.
          </dd>

          <dt id="ping">
            <a href="#ping">
              <code>ping</code>
            </a>
          </dt>
          <dd>
            A space-separated list of URLs. When the link is followed, the
            browser will send <code>POST</code> requests with the body{' '}
            <code>PING</code> to the URLs. Typically for tracking.
          </dd>

          <dt id="referrerpolicy">
            <a href="#referrerpolicy">
              <code>referrerpolicy</code>
            </a>
          </dt>
          <dd>How much of the referrer to send when following the link.</dd>

          <dt id="rel">
            <a href="#rel">
              <code>rel</code>
            </a>
          </dt>
          <dd>
            The relationship of the linked URL as space-separated link types.
          </dd>

          <dt id="target">
            <a href="#target">
              <code>target</code>
            </a>
          </dt>
          <dd>
            Where to display the linked URL, as the name for a browsing context
            (a tab, window, or <code>&lt;iframe&gt;</code>).
          </dd>
        </dl>
      </section>

      <section id="accessibility" className="content-section">
        <h2 className="section-heading">Accessibility</h2>
        <p>
          Strong link text benefits all users, especially those using screen
          readers. Avoid generic text like "click here" and describe the link's
          destination instead.
        </p>
      </section>

      <section id="examples" className="content-section">
        <h2 className="section-heading">Examples</h2>
        <h3 className="sub-heading">Linking to an absolute URL</h3>
        <pre className="block-code">
{`<a href="https://www.mozilla.com">Mozilla</a>`}
        </pre>
        <h3 className="sub-heading">Linking to relative URLs</h3>
        <pre className="block-code">
{`<a href="//example.com">Scheme-relative URL</a>
<a href="/en-US/docs/Web/HTML">Origin-relative URL</a>
<a href="p">Directory-relative URL</a>`}
        </pre>
      </section>

      <section id="security_and_privacy" className="content-section">
        <h2 className="section-heading">Security and privacy</h2>
        <p>
          <code>&lt;a&gt;</code> elements can have consequences for users'
          security and privacy. Use <code>rel="noopener"</code> or{' '}
          <code>rel="noreferrer"</code> when linking to untrusted content.
        </p>
      </section>

      <section id="technical_summary" className="content-section">
        <h2 className="section-heading">Technical summary</h2>
        <table className="summary-table">
          <tbody>
            <tr>
              <th>Content categories</th>
              <td>
                Flow content, phrasing content, interactive content, palpable
                content.
              </td>
            </tr>
            <tr>
              <th>Permitted content</th>
              <td>Transparent, containing either flow or phrasing content.</td>
            </tr>
            <tr>
              <th>Tag omission</th>
              <td>None, both the starting and ending tag are mandatory.</td>
            </tr>
            <tr>
              <th>DOM interface</th>
              <td>
                <code>HTMLAnchorElement</code>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section id="specifications" className="content-section">
        <h2 className="section-heading">Specifications</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Specification</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>HTML Standard # the-a-element</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section id="browser_compatibility" className="content-section">
        <h2 className="section-heading">Browser compatibility</h2>
        <p>
          The <code>&lt;a&gt;</code> element is supported in all major browsers,
          including Chrome, Edge, Firefox, Safari, and Opera.
        </p>
      </section>

      <section id="see_also" className="content-section">
        <h2 className="section-heading">See also</h2>
        <ul>
          <li>
            <a href="/en-US/docs/Web/CSS">
              Other elements that are somehow related to the <code>&lt;a&gt;</code>{' '}
              element
            </a>
          </li>
          <li>
            <a href="/en-US/docs/Web/HTML/Reference/Elements/link">
              The <code>&lt;link&gt;</code> element
            </a>
          </li>
        </ul>
      </section>
    </>
  )
}

===FILE: src/styles/global.css===
* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: rgb(0, 0, 0);
  background-color: rgb(255, 255, 255);
  -webkit-font-smoothing: antialiased;
}

code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875em;
}

a {
  color: rgb(4, 76, 159);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

h1,
h2,
h3 {
  font-weight: 600;
  line-height: 1.2;
}

:target {
  scroll-margin-top: 80px;
}

===FILE: src/styles/app.css===
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  background: rgb(4, 76, 159);
  color: #fff;
  padding: 8px 16px;
  z-index: 1000;
}

.skip-link:focus {
  left: 8px;
  top: 8px;
}

.page {
  display: flex;
  max-width: 1440px;
  margin: 0 auto;
  align-items: flex-start;
}

.main-area {
  display: flex;
  flex: 1;
  min-width: 0;
  gap: 24px;
  padding: 24px 32px;
}

.article {
  flex: 1;
  min-width: 0;
  max-width: 800px;
}

@media (max-width: 1100px) {
  .toc {
    display: none;
  }
}

@media (max-width: 860px) {
  .left-sidebar {
    display: none;
  }
  .main-area {
    padding: 16px;
  }
}

===FILE: src/styles/header.css===
.site-header {
  border-bottom: 1px solid rgb(237, 238, 240);
  background: rgb(255, 255, 255);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  display: flex;
  align-items: center;
  gap: 20px;
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 24px;
  height: 56px;
}

.logo {
  display: inline-flex;
  align-items: baseline;
  font-size: 24px;
  font-weight: 700;
  color: rgb(0, 0, 0);
  letter-spacing: -0.5px;
}

.logo:hover {
  text-decoration: none;
}

.logo-underscore {
  color: rgb(4, 76, 159);
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item {
  position: relative;
}

.nav-button {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  font-family: inherit;
  font-size: 16px;
  color: rgb(0, 0, 0);
  padding: 8px 10px;
  cursor: pointer;
  border-radius: 4px;
}

.nav-button:hover,
.nav-button.active {
  background: rgb(247, 247, 248);
  text-decoration: none;
}

.chevron {
  font-size: 10px;
  color: rgb(81, 86, 93);
}

.nav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 200px;
  background: #fff;
  border: 1px solid rgb(237, 238, 240);
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  padding: 8px 0;
  z-index: 200;
}

.nav-dropdown a {
  display: block;
  padding: 8px 16px;
  color: rgb(0, 0, 0);
  font-size: 15px;
}

.nav-dropdown a:hover {
  background: rgb(247, 247, 248);
  text-decoration: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

.search-input {
  font-family: inherit;
  font-size: 14px;
  padding: 7px 12px;
  border: 1px solid rgb(237, 238, 240);
  border-radius: 6px;
  background: rgb(247, 247, 248);
  width: 180px;
}

.search-input:focus {
  outline: 2px solid rgb(4, 76, 159);
  background: #fff;
}

.theme-button,
.lang-button {
  background: none;
  border: 1px solid transparent;
  font-family: inherit;
  font-size: 14px;
  color: rgb(0, 0, 0);
  padding: 7px 10px;
  cursor: pointer;
  border-radius: 6px;
}

.theme-button:hover,
.lang-button:hover {
  background: rgb(247, 247, 248);
}

@media (max-width: 860px) {
  .main-nav,
  .search-input {
    display: none;
  }
}

===FILE: src/styles/breadcrumb.css===
.breadcrumb {
  margin-bottom: 16px;
}

.breadcrumb-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 14px;
}

.breadcrumb-list li {
  display: inline-flex;
  align-items: center;
}

.breadcrumb-list .sep {
  margin: 0 8px;
  color: rgb(81, 86, 93);
}

.breadcrumb-list .current {
  color: rgb(81, 86, 93);
  font-weight: 500;
}

.breadcrumb-list .current:hover {
  text-decoration: none;
}

===FILE: src/styles/sidebar.css===
.left-sidebar {
  width: 280px;
  flex-shrink: 0;
  border-right: 1px solid rgb(237, 238, 240);
  padding: 24px 16px;
  position: sticky;
  top: 56px;
  align-self: flex-start;
  max-height: calc(100vh - 56px);
  overflow-y: auto;
}

.sidebar-filter {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-input {
  font-family: inherit;
  font-size: 14px;
  padding: 7px 12px;
  border: 1px solid rgb(237, 238, 240);
  border-radius: 6px;
  width: 100%;
}

.filter-input:focus {
  outline: 2px solid rgb(4, 76, 159);
}

.add-button {
  font-family: inherit;
  font-size: 14px;
  text-align: left;
  background: none;
  border: none;
  color: rgb(4, 76, 159);
  cursor: pointer;
  padding: 4px 0;
}

.add-button:hover {
  text-decoration: underline;
}

.sidebar-heading {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: rgb(81, 86, 93);
  margin: 0 0 8px;
}

.sidebar-group summary {
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  padding: 6px 0;
  list-style-position: inside;
}

.sidebar-list {
  list-style: none;
  margin: 4px 0 0;
  padding: 0 0 0 8px;
}

.sidebar-list li {
  margin: 0;
}

.sidebar-link {
  display: block;
  padding: 5px 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: rgb(4, 76, 159);
  border-radius: 4px;
}

.sidebar-link:hover {
  background: rgb(247, 247, 248);
  text-decoration: none;
}

.sidebar-link.active {
  background: rgb(236, 244, 254);
  font-weight: 600;
}

===FILE: src/styles/toc.css===
.toc {
  width: 220px;
  flex-shrink: 0;
}

.toc-sticky {
  position: sticky;
  top: 80px;
}

.toc-title {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: rgb(81, 86, 93);
  margin: 0 0 12px;
}

.toc-list {
  list-style: none;
  margin: 0;
  padding: 0;
  border-left: 1px solid rgb(237, 238, 240);
}

.toc-list li {
  margin: 0;
}

.toc-list a {
  display: block;
  padding: 6px 12px;
  font-size: 14px;
  color: rgb(81, 86, 93);
  border-left: 2px solid transparent;
  margin-left: -1px;
}

.toc-list a:hover {
  color: rgb(4, 76, 159);
  border-left-color: rgb(4, 76, 159);
  text-decoration: none;
}

===FILE: src/styles/content.css===
.page-title {
  font-size: 40px;
  margin: 8px 0 16px;
  font-weight: 700;
}

.page-title code {
  font-size: 0.85em;
}

.baseline-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgb(230, 244, 234);
  border: 1px solid rgb(206, 234, 214);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 24px;
  font-size: 14px;
}

.baseline-check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #00853f;
  color: #fff;
  font-size: 13px;
  flex-shrink: 0;
}

.content-section {
  margin-top: 40px;
}

.section-heading {
  font-size: 32px;
  margin: 0 0 16px;
  padding-bottom: 4px;
  border-bottom: 1px solid rgb(237, 238, 240);
  font-weight: 600;
}

.sub-heading {
  font-size: 24px;
  margin: 28px 0 12px;
  font-weight: 600;
}

p {
  margin: 0 0 16px;
}

code {
  background: rgb(237, 238, 240);
  padding: 2px 5px;
  border-radius: 4px;
}

.page-title code,
.section-heading code,
.sub-heading code {
  background: none;
  padding: 0;
}

.demo-box {
  border: 1px solid rgb(237, 238, 240);
  border-radius: 8px;
  overflow: hidden;
}

.demo-tabs {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgb(247, 247, 248);
  padding: 8px;
  border-bottom: 1px solid rgb(237, 238, 240);
}

.demo-tab {
  font-family: inherit;
  font-size: 13px;
  background: none;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  color: rgb(81, 86, 93);
}

.demo-tab.active {
  background: #fff;
  color: rgb(0, 0, 0);
  font-weight: 600;
}

.demo-reset {
  margin-left: auto;
  font-family: inherit;
  font-size: 13px;
  background: none;
  border: 1px solid rgb(237, 238, 240);
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.demo-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.demo-code {
  margin: 0;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  background: rgb(247, 247, 248);
  white-space: pre-wrap;
  overflow-x: auto;
  border-right: 1px solid rgb(237, 238, 240);
}

.demo-output {
  padding: 16px;
  font-size: 14px;
}

.demo-output ul {
  margin: 8px 0;
  padding-left: 20px;
}

.attr-list {
  margin: 16px 0;
}

.attr-list dt {
  margin-top: 16px;
  font-size: 16px;
}

.attr-list dt code {
  background: rgb(237, 238, 240);
}

.attr-list dd {
  margin: 6px 0 0;
  color: rgb(0, 0, 0);
}

.badge {
  display: inline-block;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  vertical-align: middle;
  margin-left: 6px;
  font-weight: 500;
}

.badge.experimental {
  background: rgb(236, 244, 254);
  color: rgb(4, 76, 159);
}

.block-code {
  background: rgb(247, 247, 248);
  border: 1px solid rgb(237, 238, 240);
  border-radius: 8px;
  padding: 16px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  overflow-x: auto;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  margin: 12px 0;
}

.summary-table th,
.summary-table td {
  border: 1px solid rgb(237, 238, 240);
  padding: 10px 12px;
  text-align: left;
  vertical-align: top;
}

.summary-table th {
  background: rgb(247, 247, 248);
  font-weight: 600;
  white-space: nowrap;
}

ul {
  margin: 0 0 16px;
  padding-left: 24px;
}

li {
  margin: 4px 0;
}