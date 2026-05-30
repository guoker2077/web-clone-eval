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
    "vite": "^5.4.2"
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
    "strict": true,
    "noEmit": true
  },
  "include": ["vite.config.ts"]
}

===FILE: index.html===
<!doctype html>
<html lang="en">
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
import App from './App.tsx'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

===FILE: src/index.css===
*,
*::before,
*::after {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: rgb(0, 0, 0);
  background-color: rgb(255, 255, 255);
  -webkit-font-smoothing: antialiased;
}

a {
  color: rgb(4, 76, 159);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code,
pre {
  font-family: 'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono',
    Menlo, monospace;
}

===FILE: src/data.ts===
export interface NavItem {
  label: string
  href?: string
  isMenu?: boolean
  testid?: string
}

export const headerNav: NavItem[] = [
  { label: 'HTML', isMenu: true, testid: 'nav-html-menu' },
  { label: 'CSS', isMenu: true },
  { label: 'JavaScript', isMenu: true },
  { label: 'Web APIs', isMenu: true },
  { label: 'Learn', isMenu: true, testid: 'nav-learn-menu' },
  { label: 'Plus', isMenu: true },
  { label: 'About', href: '/en-US/about/' },
  { label: 'Blog', href: '/en-US/blog/', testid: 'nav-blog' },
]

export const elementList: string[] = [
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
  '<blockquote>',
  '<body>',
  '<br>',
  '<button>',
]

export interface TocItem {
  id: string
  label: string
  testid: string
}

export const tocItems: TocItem[] = [
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
  {
    id: 'specifications',
    label: 'Specifications',
    testid: 'toc-specifications',
  },
  {
    id: 'browser_compatibility',
    label: 'Browser compatibility',
    testid: 'toc-browser-compatibility',
  },
  { id: 'see_also', label: 'See also', testid: 'toc-see-also' },
]

===FILE: src/App.tsx===
import Header from './components/Header'
import LeftSidebar from './components/LeftSidebar'
import Article from './components/Article'
import Toc from './components/Toc'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <Header />
      <div className="layout">
        <LeftSidebar />
        <main id="content" className="main-column" data-testid="main-content">
          <Article />
        </main>
        <Toc />
      </div>
    </div>
  )
}

===FILE: src/components/Header.tsx===
import { headerNav } from '../data'

export default function Header() {
  return (
    <>
      <a href="#content" className="skip-link" data-testid="skip-to-content">
        Skip to main content
      </a>

      <div className="promo-banner">
        <div className="promo-inner">
          <span className="promo-text">
            Build, deploy, and scale AI agents and autonomous servers. Three is
            the platform builders trust with critical workloads.
          </span>
          <button type="button" className="promo-btn">
            Get started
          </button>
          <a href="/en-US/plus" className="promo-noads">
            Don't want to see ads?
          </a>
        </div>
      </div>

      <header className="site-header">
        <div className="header-inner">
          <a
            href="/en-US/"
            className="logo"
            aria-label="MDN homepage"
            data-testid="logo-home"
          >
            <span className="logo-text">MDN</span>
            <span className="logo-cursor">_</span>
          </a>

          <nav className="main-nav" aria-label="Main menu">
            {headerNav.map((item) =>
              item.isMenu ? (
                <button
                  key={item.label}
                  type="button"
                  className="nav-btn"
                  data-testid={item.testid}
                >
                  {item.label}
                  <span className="caret" aria-hidden="true">
                    ▾
                  </span>
                </button>
              ) : (
                <a
                  key={item.label}
                  href={item.href}
                  className="nav-link"
                  data-testid={item.testid}
                >
                  {item.label}
                </a>
              ),
            )}
          </nav>

          <div className="header-tools">
            <button type="button" className="theme-btn" aria-label="Theme">
              <span className="theme-icon" aria-hidden="true">
                ◐
              </span>
              Theme
            </button>
            <form
              className="search-form"
              role="search"
              onSubmit={(e) => e.preventDefault()}
            >
              <input
                type="search"
                className="search-input"
                placeholder="Search MDN"
                aria-label="Search MDN"
                data-testid="search-input"
              />
            </form>
            <button type="button" className="lang-btn">
              English (US)
            </button>
          </div>
        </div>
      </header>
    </>
  )
}

===FILE: src/components/LeftSidebar.tsx===
import { useState } from 'react'
import { elementList } from '../data'

export default function LeftSidebar() {
  const [filter, setFilter] = useState('')

  const filtered = elementList.filter((el) =>
    el.toLowerCase().includes(filter.toLowerCase()),
  )

  return (
    <aside className="left-sidebar" aria-label="Reference">
      <div className="sidebar-filter">
        <input
          type="text"
          className="filter-input"
          placeholder="Filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          aria-label="Filter sidebar"
          data-testid="sidebar-filter"
        />
      </div>

      <div className="sidebar-section">
        <p className="sidebar-heading">Reference</p>
        <p className="sidebar-subheading">Elements</p>
        <ul className="element-list">
          {filtered.map((el) => (
            <li key={el}>
              <a
                href={`/en-US/docs/Web/HTML/Reference/Elements/${el
                  .replace('<', '')
                  .replace('>', '')}`}
                className={el === '<a>' ? 'element-link active' : 'element-link'}
                aria-current={el === '<a>' ? 'page' : undefined}
              >
                <code>{el}</code>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  )
}

===FILE: src/components/Toc.tsx===
import { tocItems } from '../data'

export default function Toc() {
  return (
    <aside className="toc" aria-label="In this article">
      <div className="toc-sticky">
        <p className="toc-title">In this article</p>
        <ul className="toc-list" data-testid="toc-list">
          {tocItems.map((item) => (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                className="toc-link"
                data-testid={item.testid}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="ad-box">
          <p className="ad-label">Ad</p>
          <p className="ad-title">Auth0</p>
          <p className="ad-copy">
            Drop-in auth for AI agents. Get authorization and secure access
            controls for your AI apps.
          </p>
          <button type="button" className="ad-btn">
            Start Building
          </button>
        </div>
      </div>
    </aside>
  )
}

===FILE: src/components/Article.tsx===
export default function Article() {
  return (
    <article className="article">
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <ol>
          <li>
            <a href="/en-US/docs/Web" data-testid="breadcrumb-web">
              Web
            </a>
          </li>
          <li>
            <a href="/en-US/docs/Web/HTML" data-testid="breadcrumb-html">
              HTML
            </a>
          </li>
          <li>
            <a
              href="/en-US/docs/Web/HTML/Reference"
              data-testid="breadcrumb-reference"
            >
              Reference
            </a>
          </li>
          <li>
            <a
              href="/en-US/docs/Web/HTML/Reference/Elements"
              data-testid="breadcrumb-elements"
            >
              Elements
            </a>
          </li>
          <li>
            <a
              href="/en-US/docs/Web/HTML/Reference/Elements/a"
              aria-current="page"
              data-testid="breadcrumb-anchor"
            >
              &lt;a&gt;
            </a>
          </li>
        </ol>
      </nav>

      <h1 className="page-title">
        <code className="title-code">&lt;a&gt;</code>: The Anchor element
      </h1>

      <div className="baseline">
        <span className="baseline-icon" aria-hidden="true">
          ✓
        </span>
        <span className="baseline-text">
          <strong>Baseline</strong> Widely available
        </span>
      </div>

      <p>
        The <code>&lt;a&gt;</code> HTML element (or <em>anchor</em> element),
        with its <code>href</code> attribute, creates a hyperlink to web pages,
        files, email addresses, locations in the same page, or anything else a
        URL can address.
      </p>

      <p>
        Content within each <code>&lt;a&gt;</code> <em>should</em> indicate the
        link's destination. If the <code>href</code> attribute is present,
        pressing the enter key while focused on the <code>&lt;a&gt;</code>{' '}
        element will activate it.
      </p>

      <h2 id="try_it" className="section-heading">
        Try it
      </h2>
      <div className="demo">
        <div className="demo-editor">
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
          <pre className="demo-code">
            <code>{`<p>You can reach Michael at:</p>

<ul>
  <li><a href="https://example.com">Website</a></li>
  <li><a href="mailto:m.bluth@example.com">Email</a></li>
  <li><a href="tel:+123456789">Phone</a></li>
</ul>`}</code>
          </pre>
        </div>
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

      <h2 id="attributes" className="section-heading">
        Attributes
      </h2>
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
          with or without a <code>filename</code> value. Without a value, the
          browser will suggest a filename/extension, generated from various
          sources.
        </dd>

        <dt id="href">
          <a href="#href">
            <code>href</code>
          </a>
        </dt>
        <dd>
          The URL that the hyperlink points to. Links are not restricted to
          HTTP-based URLs — they can use any URL scheme supported by browsers:
          telephone numbers with <code>tel:</code> URLs, email addresses with{' '}
          <code>mailto:</code> URLs, and document fragments.
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
          A space-separated list of URLs. When the link is followed, the browser
          will send <code>POST</code> requests with the body <code>PING</code>{' '}
          to the URLs. Typically for tracking.
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
          Where to display the linked URL, as the name for a browsing context (a
          tab, window, or <code>&lt;iframe&gt;</code>).
        </dd>

        <dt id="type">
          <a href="#type">
            <code>type</code>
          </a>
        </dt>
        <dd>
          Hints at the linked URL's format with a MIME type. No built-in
          functionality.
        </dd>
      </dl>

      <div className="note">
        <p>
          <strong>Note:</strong> You can use the{' '}
          <code>chrome://flags</code> page in Chromium-based browsers to enable
          or disable experimental attribution features.
        </p>
      </div>

      <h2 id="accessibility" className="section-heading">
        Accessibility
      </h2>
      <h3>Strong link text</h3>
      <p>
        The content inside a link should indicate where the link goes, even out
        of context. Avoid using uninformative link phrasing such as "click
        here" or "read more".
      </p>

      <h2 id="examples" className="section-heading">
        Examples
      </h2>
      <h3>Linking to an absolute URL</h3>
      <pre className="code-block">
        <code>{`<a href="https://www.mozilla.com">Mozilla</a>`}</code>
      </pre>
      <h3>Linking to relative URLs</h3>
      <pre className="code-block">
        <code>{`<!-- Linking to a page in the same directory -->
<a href="./about.html">About this site</a>`}</code>
      </pre>

      <h2 id="security_and_privacy" className="section-heading">
        Security and privacy
      </h2>
      <p>
        <code>&lt;a&gt;</code> elements can have consequences for users'
        security and privacy. See the{' '}
        <code>Referer</code> header documentation for information on mitigating
        these. Linking to a third-party resource with{' '}
        <code>target="_blank"</code> can expose your site to performance and
        security issues; always add <code>rel="noopener"</code>.
      </p>

      <h2 id="technical_summary" className="section-heading">
        Technical summary
      </h2>
      <table className="tech-table">
        <tbody>
          <tr>
            <th scope="row">Content categories</th>
            <td>
              Flow content, phrasing content, interactive content, palpable
              content.
            </td>
          </tr>
          <tr>
            <th scope="row">Permitted content</th>
            <td>
              Transparent, containing either flow content or phrasing content.
            </td>
          </tr>
          <tr>
            <th scope="row">Tag omission</th>
            <td>None, both the starting and ending tag are mandatory.</td>
          </tr>
          <tr>
            <th scope="row">Permitted parents</th>
            <td>Any element that accepts phrasing content, or any flow content.</td>
          </tr>
          <tr>
            <th scope="row">Implicit ARIA role</th>
            <td>
              link when <code>href</code> attribute is present, otherwise{' '}
              generic
            </td>
          </tr>
          <tr>
            <th scope="row">DOM interface</th>
            <td>
              <code>HTMLAnchorElement</code>
            </td>
          </tr>
        </tbody>
      </table>

      <h2 id="specifications" className="section-heading">
        Specifications
      </h2>
      <table className="tech-table">
        <thead>
          <tr>
            <th scope="col">Specification</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <a href="https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-a-element">
                HTML Standard # the-a-element
              </a>
            </td>
          </tr>
        </tbody>
      </table>

      <h2 id="browser_compatibility" className="section-heading">
        Browser compatibility
      </h2>
      <div className="bcd">
        <div className="bcd-row bcd-head">
          <span className="bcd-feature" />
          <span className="bcd-browser">Chrome</span>
          <span className="bcd-browser">Edge</span>
          <span className="bcd-browser">Firefox</span>
          <span className="bcd-browser">Safari</span>
        </div>
        <div className="bcd-row">
          <span className="bcd-feature">
            <code>a</code>
          </span>
          <span className="bcd-cell yes">1</span>
          <span className="bcd-cell yes">12</span>
          <span className="bcd-cell yes">1</span>
          <span className="bcd-cell yes">1</span>
        </div>
        <div className="bcd-row">
          <span className="bcd-feature">
            <code>download</code>
          </span>
          <span className="bcd-cell yes">14</span>
          <span className="bcd-cell yes">18</span>
          <span className="bcd-cell yes">20</span>
          <span className="bcd-cell no">No</span>
        </div>
        <div className="bcd-row">
          <span className="bcd-feature">
            <code>href</code>
          </span>
          <span className="bcd-cell yes">1</span>
          <span className="bcd-cell yes">12</span>
          <span className="bcd-cell yes">1</span>
          <span className="bcd-cell yes">1</span>
        </div>
      </div>

      <h2 id="see_also" className="section-heading">
        See also
      </h2>
      <ul className="see-also-list">
        <li>
          <a href="/en-US/docs/Web/HTTP/Headers">
            HTTP <code>Link</code> header
          </a>
          , which provides similar functionality in HTTP headers
        </li>
        <li>
          <a href="/en-US/docs/Web/HTML/Reference/Elements/link">
            <code>&lt;link&gt;</code>
          </a>{' '}
          element
        </li>
      </ul>
    </article>
  )
}

===FILE: src/App.css===
.app {
  width: 100%;
}

/* ---------- Skip link ---------- */
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  z-index: 1000;
  background: #fff;
  color: rgb(4, 76, 159);
  padding: 0.5rem 1rem;
  border: 2px solid rgb(4, 76, 159);
  border-radius: 4px;
}
.skip-link:focus {
  left: 1rem;
  top: 0.5rem;
}

/* ---------- Promo banner ---------- */
.promo-banner {
  background: rgb(0, 0, 0);
  color: #fff;
  font-size: 0.8125rem;
}
.promo-inner {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 1rem;
}
.promo-text {
  flex: 1;
  color: rgb(237, 238, 240);
}
.promo-btn {
  background: #fff;
  color: #000;
  border: none;
  border-radius: 4px;
  padding: 0.3rem 0.9rem;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}
.promo-noads {
  color: rgb(206, 209, 214);
  font-size: 0.6875rem;
  white-space: nowrap;
}

/* ---------- Header ---------- */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  border-bottom: 1px solid rgb(237, 238, 240);
}
.header-inner {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.5rem 1rem;
}
.logo {
  display: inline-flex;
  align-items: baseline;
  font-weight: 700;
  font-size: 1.5rem;
  color: #000;
  text-decoration: none;
  letter-spacing: -0.02em;
}
.logo:hover {
  text-decoration: none;
}
.logo-cursor {
  color: #000;
}
.main-nav {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex: 1;
}
.nav-btn,
.nav-link {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgb(33, 33, 33);
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
}
.nav-btn:hover,
.nav-link:hover {
  background: rgb(247, 247, 248);
  text-decoration: none;
}
.caret {
  font-size: 0.625rem;
  color: rgb(81, 86, 93);
}
.header-tools {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.theme-btn,
.lang-btn {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.8125rem;
  color: rgb(33, 33, 33);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.4rem 0.5rem;
  border-radius: 4px;
}
.theme-btn:hover,
.lang-btn:hover {
  background: rgb(247, 247, 248);
}
.theme-icon {
  font-size: 1rem;
}
.search-input {
  font-family: inherit;
  font-size: 0.8125rem;
  border: 1px solid rgb(210, 213, 218);
  border-radius: 4px;
  padding: 0.4rem 0.75rem;
  width: 180px;
  background: rgb(247, 247, 248);
}
.search-input:focus {
  outline: 2px solid rgb(4, 76, 159);
  background: #fff;
}

/* ---------- Layout ---------- */
.layout {
  max-width: 1440px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr) 15rem;
  align-items: start;
}

/* ---------- Left sidebar ---------- */
.left-sidebar {
  position: sticky;
  top: 56px;
  align-self: start;
  max-height: calc(100vh - 56px);
  overflow-y: auto;
  border-right: 1px solid rgb(237, 238, 240);
  padding: 1rem 0.75rem;
  font-size: 0.875rem;
}
.sidebar-filter {
  margin-bottom: 1rem;
}
.filter-input {
  width: 100%;
  font-family: inherit;
  font-size: 0.8125rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid rgb(210, 213, 218);
  border-radius: 4px;
  background: rgb(247, 247, 248);
}
.filter-input:focus {
  outline: 2px solid rgb(4, 76, 159);
  background: #fff;
}
.sidebar-heading {
  font-weight: 700;
  font-size: 0.9375rem;
  margin: 0.5rem 0 0.25rem;
}
.sidebar-subheading {
  font-weight: 600;
  font-size: 0.8125rem;
  color: rgb(81, 86, 93);
  margin: 0.75rem 0 0.4rem;
}
.element-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.element-list li {
  margin: 0;
}
.element-link {
  display: block;
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  color: rgb(33, 33, 33);
  border-left: 3px solid transparent;
}
.element-link code {
  font-size: 0.8125rem;
}
.element-link:hover {
  background: rgb(247, 247, 248);
  text-decoration: none;
}
.element-link.active {
  background: rgb(236, 244, 254);
  border-left-color: rgb(4, 76, 159);
  font-weight: 600;
}
.element-link.active code {
  color: rgb(4, 76, 159);
}

/* ---------- Main column ---------- */
.main-column {
  min-width: 0;
  padding: 1.5rem 2.5rem;
}
.article {
  max-width: 50rem;
}

/* ---------- Breadcrumb ---------- */
.breadcrumb ol {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin: 0 0 1.25rem;
  padding: 0;
  font-size: 0.8125rem;
}
.breadcrumb li:not(:last-child)::after {
  content: '/';
  color: rgb(81, 86, 93);
  margin-left: 0.4rem;
}
.breadcrumb a {
  color: rgb(4, 76, 159);
}
.breadcrumb li:last-child a {
  color: rgb(81, 86, 93);
}

/* ---------- Title ---------- */
.page-title {
  font-size: 2.5rem;
  line-height: 1.2;
  font-weight: 600;
  margin: 0 0 1rem;
}
.title-code {
  font-size: 2.25rem;
  background: rgb(237, 238, 240);
  padding: 0 0.25rem;
  border-radius: 4px;
}

/* ---------- Baseline ---------- */
.baseline {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: rgb(230, 244, 234);
  border-radius: 6px;
  padding: 0.6rem 1rem;
  margin-bottom: 1.5rem;
  font-size: 0.9375rem;
}
.baseline-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.4rem;
  height: 1.4rem;
  border-radius: 50%;
  background: rgb(206, 234, 214);
  color: rgb(20, 110, 60);
  font-size: 0.85rem;
  font-weight: 700;
}
.baseline-text strong {
  font-weight: 700;
}

/* ---------- Paragraphs / headings ---------- */
.article p {
  margin: 0 0 1rem;
}
.section-heading {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 2.5rem 0 1rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid rgb(237, 238, 240);
  scroll-margin-top: 70px;
}
.article h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 1.5rem 0 0.75rem;
}
.article code {
  background: rgb(237, 238, 240);
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-size: 0.875em;
}

/* ---------- Try it demo ---------- */
.demo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border: 1px solid rgb(237, 238, 240);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.demo-editor {
  background: rgb(247, 247, 248);
  border-right: 1px solid rgb(237, 238, 240);
}
.demo-tabs {
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgb(237, 238, 240);
  background: #fff;
}
.demo-tab {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.8125rem;
  padding: 0.6rem 1rem;
  cursor: pointer;
  color: rgb(81, 86, 93);
  border-bottom: 2px solid transparent;
}
.demo-tab.active {
  color: #000;
  border-bottom-color: rgb(4, 76, 159);
  font-weight: 600;
}
.demo-reset {
  margin-left: auto;
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.8125rem;
  padding: 0.6rem 1rem;
  cursor: pointer;
  color: rgb(4, 76, 159);
}
.demo-code {
  margin: 0;
  padding: 1rem;
  font-size: 0.8125rem;
  line-height: 1.5;
  overflow-x: auto;
  color: rgb(33, 33, 33);
}
.demo-code code {
  background: none;
  padding: 0;
}
.demo-output {
  padding: 1rem;
  background: #fff;
}
.demo-output ul {
  padding-left: 1.2rem;
}

/* ---------- Attribute list ---------- */
.attr-list {
  margin: 0 0 1.5rem;
}
.attr-list dt {
  margin-top: 1.25rem;
  font-weight: 500;
}
.attr-list dt code {
  background: rgb(237, 238, 240);
}
.attr-list dd {
  margin: 0.4rem 0 0;
  color: rgb(33, 33, 33);
}
.badge {
  font-size: 0.6875rem;
  padding: 0.05rem 0.4rem;
  border-radius: 3px;
  vertical-align: middle;
}
.badge.experimental {
  background: rgb(236, 244, 254);
  color: rgb(4, 76, 159);
}

/* ---------- Note ---------- */
.note {
  background: rgb(236, 244, 254);
  border-left: 4px solid rgb(4, 76, 159);
  padding: 0.75rem 1rem;
  border-radius: 0 4px 4px 0;
  margin: 1.5rem 0;
}
.note p {
  margin: 0;
  font-size: 0.9375rem;
}

/* ---------- Code block ---------- */
.code-block {
  background: rgb(247, 247, 248);
  border: 1px solid rgb(237, 238, 240);
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
  font-size: 0.8125rem;
  margin: 0 0 1.25rem;
}
.code-block code {
  background: none;
  padding: 0;
}

/* ---------- Tables ---------- */
.tech-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 1.5rem;
  font-size: 0.875rem;
}
.tech-table th,
.tech-table td {
  border: 1px solid rgb(237, 238, 240);
  padding: 0.6rem 0.75rem;
  text-align: left;
  vertical-align: top;
}
.tech-table th[scope='row'] {
  background: rgb(247, 247, 248);
  width: 14rem;
  font-weight: 600;
}
.tech-table th[scope='col'] {
  background: rgb(247, 247, 248);
}

/* ---------- BCD ---------- */
.bcd {
  border: 1px solid rgb(237, 238, 240);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  font-size: 0.8125rem;
}
.bcd-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  border-bottom: 1px solid rgb(237, 238, 240);
}
.bcd-row:last-child {
  border-bottom: none;
}
.bcd-head {
  background: rgb(247, 247, 248);
  font-weight: 600;
}
.bcd-feature,
.bcd-browser,
.bcd-cell {
  padding: 0.5rem 0.75rem;
  border-right: 1px solid rgb(237, 238, 240);
}
.bcd-cell:last-child,
.bcd-browser:last-child {
  border-right: none;
}
.bcd-cell.yes {
  background: rgb(230, 244, 234);
  color: rgb(20, 110, 60);
}
.bcd-cell.no {
  background: rgb(247, 247, 248);
  color: rgb(81, 86, 93);
}

.see-also-list {
  margin: 0 0 2rem;
  padding-left: 1.2rem;
}
.see-also-list li {
  margin-bottom: 0.4rem;
}

/* ---------- Right TOC ---------- */
.toc {
  padding: 1.5rem 1rem;
}
.toc-sticky {
  position: sticky;
  top: 70px;
}
.toc-title {
  font-weight: 700;
  font-size: 0.9375rem;
  margin: 0 0 0.75rem;
}
.toc-list {
  list-style: none;
  margin: 0 0 1.5rem;
  padding: 0;
  border-left: 1px solid rgb(237, 238, 240);
}
.toc-link {
  display: block;
  padding: 0.3rem 0 0.3rem 0.75rem;
  font-size: 0.8125rem;
  color: rgb(81, 86, 93);
  margin-left: -1px;
  border-left: 2px solid transparent;
}
.toc-link:hover {
  color: rgb(4, 76, 159);
  text-decoration: none;
  border-left-color: rgb(4, 76, 159);
}

/* ---------- Ad box ---------- */
.ad-box {
  border: 1px solid rgb(237, 238, 240);
  border-radius: 6px;
  padding: 1rem;
  font-size: 0.8125rem;
}
.ad-label {
  font-size: 0.6875rem;
  color: rgb(81, 86, 93);
  text-transform: uppercase;
  margin: 0 0 0.5rem;
}
.ad-title {
  font-weight: 700;
  font-size: 1rem;
  margin: 0 0 0.5rem;
}
.ad-copy {
  color: rgb(81, 86, 93);
  margin: 0 0 0.75rem;
  line-height: 1.4;
}
.ad-btn {
  background: rgb(4, 76, 159);
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
}

/* ---------- Responsive ---------- */
@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 14rem minmax(0, 1fr);
  }
  .toc {
    display: none;
  }
}
@media (max-width: 800px) {
  .layout {
    grid-template-columns: 1fr;
  }
  .left-sidebar {
    display: none;
  }
  .main-nav {
    display: none;
  }
  .demo {
    grid-template-columns: 1fr;
  }
}