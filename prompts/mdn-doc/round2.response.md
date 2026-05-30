===FILE: package.json===
{
  "name": "mdn-a-element-clone",
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
    "strict": true,
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
import './App.css'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Breadcrumb from './components/Breadcrumb'
import Article from './components/Article'
import Toc from './components/Toc'

export default function App() {
  return (
    <>
      <a className="skip-link" href="#content" data-testid="skip-to-content">
        Skip to main content
      </a>
      <Header />
      <div className="page-container">
        <Sidebar />
        <div className="content-and-toc">
          <main className="main-content" id="content">
            <Breadcrumb />
            <Article />
          </main>
          <Toc />
        </div>
      </div>
      <footer className="site-footer">
        <div className="footer-inner">
          <span className="footer-logo">mdn_</span>
          <p>
            Your blueprint for a better internet. This page is a faithful study
            reproduction for layout and interaction purposes.
          </p>
        </div>
      </footer>
    </>
  )
}

===FILE: src/App.css===
.page-container {
  display: grid;
  grid-template-columns: 290px minmax(0, 1fr);
  max-width: 1440px;
  margin: 0 auto;
  width: 100%;
}

.content-and-toc {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 240px;
  gap: 0;
  min-width: 0;
}

.main-content {
  padding: 0 2.5rem 4rem;
  min-width: 0;
}

.skip-link {
  position: absolute;
  left: -999px;
  top: 0;
  z-index: 1000;
  background: #fff;
  color: var(--link);
  padding: 0.6rem 1rem;
  border: 2px solid var(--link);
  border-radius: 4px;
  text-decoration: none;
}

.skip-link:focus {
  left: 1rem;
  top: 1rem;
}

.site-footer {
  background: rgb(81, 86, 93);
  color: rgb(237, 238, 240);
  margin-top: 3rem;
}

.footer-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 2rem 2.5rem;
}

.footer-logo {
  font-weight: 700;
  font-size: 1.5rem;
  color: #fff;
  display: block;
  margin-bottom: 0.5rem;
}

.footer-inner p {
  max-width: 540px;
  font-size: 0.875rem;
  color: rgb(237, 238, 240);
}

@media (max-width: 1100px) {
  .content-and-toc {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 820px) {
  .page-container {
    grid-template-columns: minmax(0, 1fr);
  }
}

===FILE: src/styles/global.css===
:root {
  --text: rgb(27, 27, 27);
  --text-secondary: rgb(81, 86, 93);
  --link: rgb(4, 76, 159);
  --bg: rgb(255, 255, 255);
  --bg-secondary: rgb(247, 247, 248);
  --border: rgb(237, 238, 240);
  --border-strong: rgb(206, 211, 217);
  --code-bg: rgb(247, 247, 248);
  --note-bg: rgb(236, 244, 254);
  --green-bg: rgb(230, 244, 234);
  --green-bg-light: rgb(206, 234, 214);
  --mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  scroll-padding-top: 70px;
}

body {
  margin: 0;
  font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--link);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code {
  font-family: var(--mono);
  font-size: 0.85em;
}

h1,
h2,
h3,
h4 {
  scroll-margin-top: 70px;
  font-weight: 600;
  line-height: 1.2;
  color: var(--text);
}

===FILE: src/components/Header.tsx===
import './Header.css'

export default function Header() {
  return (
    <header className="site-header">
      <div className="promo-banner">
        <span className="promo-text">
          Build, deploy, and scale AI agents and autonomous security. Time is the
          platform builders trust with critical workloads.
        </span>
        <button type="button" className="promo-btn">
          Get started
        </button>
        <button type="button" className="promo-close" aria-label="Close banner">
          ×
        </button>
      </div>

      <nav className="main-nav" aria-label="Main">
        <div className="nav-left">
          <a className="logo" href="/en-US/" data-testid="logo-home" aria-label="MDN homepage">
            mdn<span className="logo-cursor">_</span>
          </a>
          <ul className="nav-list">
            <li>
              <button type="button" className="nav-item">References</button>
            </li>
            <li>
              <button type="button" className="nav-item">Guides</button>
            </li>
            <li>
              <button type="button" className="nav-item" data-testid="nav-html-menu">
                HTML
              </button>
            </li>
            <li>
              <button type="button" className="nav-item">CSS</button>
            </li>
            <li>
              <button type="button" className="nav-item">JavaScript</button>
            </li>
            <li>
              <button type="button" className="nav-item">Web APIs</button>
            </li>
            <li>
              <button type="button" className="nav-item" data-testid="nav-learn-menu">
                Learn
              </button>
            </li>
            <li>
              <button type="button" className="nav-item">Plus</button>
            </li>
            <li>
              <button type="button" className="nav-item">Tools</button>
            </li>
            <li>
              <a className="nav-item" href="/en-US/about/">About</a>
            </li>
            <li>
              <a className="nav-item" href="/en-US/blog/" data-testid="nav-blog">
                Blog
              </a>
            </li>
          </ul>
        </div>

        <div className="nav-right">
          <div className="nav-search">
            <input type="search" placeholder="Search MDN" aria-label="Search MDN" />
          </div>
          <button type="button" className="theme-btn">Theme</button>
          <button type="button" className="login-btn">Log in</button>
        </div>
      </nav>
    </header>
  )
}

===FILE: src/components/Header.css===
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
}

.promo-banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgb(0, 0, 0);
  color: #fff;
  font-size: 0.8125rem;
  padding: 0.5rem 1.5rem;
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
  padding: 0.35rem 0.9rem;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.promo-close {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 1.25rem;
  cursor: pointer;
  line-height: 1;
}

.main-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.5rem 1.5rem;
  max-width: 1440px;
  margin: 0 auto;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 0;
}

.logo {
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--text);
  letter-spacing: -0.5px;
  text-decoration: none;
  white-space: nowrap;
}

.logo:hover {
  text-decoration: none;
}

.logo-cursor {
  color: var(--link);
}

.nav-list {
  display: flex;
  align-items: center;
  gap: 0.15rem;
  list-style: none;
  margin: 0;
  padding: 0;
  flex-wrap: wrap;
}

.nav-item {
  display: inline-block;
  background: transparent;
  border: none;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text);
  padding: 0.4rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}

.nav-item:hover {
  background: var(--bg-secondary);
  text-decoration: none;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-search input {
  font-family: inherit;
  font-size: 0.8125rem;
  padding: 0.4rem 0.7rem;
  border: 1px solid var(--border-strong);
  border-radius: 4px;
  width: 150px;
  background: var(--bg-secondary);
}

.nav-search input:focus {
  outline: 2px solid var(--link);
  background: #fff;
}

.theme-btn {
  background: transparent;
  border: none;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text);
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
}

.theme-btn:hover {
  background: var(--bg-secondary);
}

.login-btn {
  background: rgb(0, 0, 0);
  color: #fff;
  border: 1px solid #000;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.4rem 0.9rem;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}

.login-btn:hover {
  opacity: 0.85;
}

@media (max-width: 1100px) {
  .nav-search input {
    width: 110px;
  }
}

@media (max-width: 820px) {
  .nav-list {
    display: none;
  }
}

===FILE: src/components/Sidebar.tsx===
import './Sidebar.css'

const elements = [
  'a',
  'abbr',
  'acronym',
  'address',
  'area',
  'article',
  'aside',
  'audio',
  'b',
  'base',
  'bdi',
  'bdo',
  'big',
  'blockquote',
  'body',
  'br',
  'button',
  'canvas',
  'caption',
  'cite',
  'code',
  'col',
  'colgroup',
  'data',
  'datalist',
  'dd',
  'del',
  'details',
  'dfn',
  'dialog',
]

export default function Sidebar() {
  return (
    <aside className="sidebar" aria-label="Reference navigation">
      <div className="sidebar-inner">
        <div className="filter-box">
          <input type="search" placeholder="Filter" aria-label="Filter sidebar" />
        </div>
        <a className="sidebar-cta" href="/en-US/docs/Web/HTML">
          Add HTML
        </a>
        <nav className="sidebar-nav">
          <p className="sidebar-heading">Reference</p>
          <details open className="sidebar-group">
            <summary>Elements</summary>
            <ul className="element-list">
              {elements.map((el) => (
                <li key={el}>
                  <a
                    className={el === 'a' ? 'element-link active' : 'element-link'}
                    href={`/en-US/docs/Web/HTML/Reference/Elements/${el}`}
                    aria-current={el === 'a' ? 'page' : undefined}
                  >
                    <code>&lt;{el}&gt;</code>
                  </a>
                </li>
              ))}
            </ul>
          </details>
        </nav>
      </div>
    </aside>
  )
}

===FILE: src/components/Sidebar.css===
.sidebar {
  border-right: 1px solid var(--border);
  background: var(--bg);
}

.sidebar-inner {
  position: sticky;
  top: 64px;
  max-height: calc(100vh - 64px);
  overflow-y: auto;
  padding: 1.25rem 1rem 2rem;
}

.filter-box input {
  width: 100%;
  font-family: inherit;
  font-size: 0.8125rem;
  padding: 0.45rem 0.7rem;
  border: 1px solid var(--border-strong);
  border-radius: 4px;
  background: var(--bg-secondary);
}

.filter-box input:focus {
  outline: 2px solid var(--link);
  background: #fff;
}

.sidebar-cta {
  display: block;
  margin: 0.75rem 0;
  padding: 0.4rem 0.6rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: 4px;
  text-align: center;
}

.sidebar-cta:hover {
  background: var(--bg-secondary);
  text-decoration: none;
}

.sidebar-heading {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
  margin: 1rem 0 0.5rem;
}

.sidebar-group summary {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text);
  padding: 0.35rem 0.4rem;
  cursor: pointer;
  border-radius: 4px;
}

.sidebar-group summary:hover {
  background: var(--bg-secondary);
}

.element-list {
  list-style: none;
  margin: 0.25rem 0 0;
  padding: 0 0 0 0.5rem;
}

.element-link {
  display: block;
  padding: 0.2rem 0.5rem;
  font-size: 0.8125rem;
  color: var(--text-secondary);
  border-radius: 4px;
  border-left: 2px solid transparent;
}

.element-link:hover {
  background: var(--bg-secondary);
  text-decoration: none;
}

.element-link.active {
  color: var(--link);
  font-weight: 600;
  background: var(--note-bg);
  border-left-color: var(--link);
}

.element-link code {
  font-size: 0.85em;
}

@media (max-width: 820px) {
  .sidebar {
    display: none;
  }
}

===FILE: src/components/Breadcrumb.tsx===
import './Breadcrumb.css'

export default function Breadcrumb() {
  return (
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
          <a href="/en-US/docs/Web/HTML/Reference" data-testid="breadcrumb-reference">
            Reference
          </a>
        </li>
        <li>
          <a href="/en-US/docs/Web/HTML/Reference/Elements" data-testid="breadcrumb-elements">
            Elements
          </a>
        </li>
        <li aria-current="page">
          <a
            href="/en-US/docs/Web/HTML/Reference/Elements/a"
            data-testid="breadcrumb-anchor"
            className="current"
          >
            &lt;a&gt;
          </a>
        </li>
      </ol>
    </nav>
  )
}

===FILE: src/components/Breadcrumb.css===
.breadcrumb {
  padding: 1rem 0 0.5rem;
  font-size: 0.8125rem;
}

.breadcrumb ol {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
}

.breadcrumb li {
  display: flex;
  align-items: center;
}

.breadcrumb li:not(:last-child)::after {
  content: '/';
  margin: 0 0.5rem;
  color: var(--text-secondary);
}

.breadcrumb a {
  color: var(--link);
}

.breadcrumb a.current {
  color: var(--text-secondary);
  font-weight: 500;
}

.breadcrumb a.current:hover {
  text-decoration: none;
  cursor: default;
}

===FILE: src/components/Toc.tsx===
import './Toc.css'

const items = [
  { id: 'try_it', label: 'Try it', testid: 'toc-try-it' },
  { id: 'attributes', label: 'Attributes', testid: 'toc-attributes' },
  { id: 'accessibility', label: 'Accessibility', testid: 'toc-accessibility' },
  { id: 'examples', label: 'Examples', testid: 'toc-examples' },
  { id: 'security_and_privacy', label: 'Security and privacy', testid: 'toc-security-privacy' },
  { id: 'technical_summary', label: 'Technical summary', testid: 'toc-technical-summary' },
  { id: 'specifications', label: 'Specifications', testid: 'toc-specifications' },
  { id: 'browser_compatibility', label: 'Browser compatibility', testid: 'toc-browser-compatibility' },
  { id: 'see_also', label: 'See also', testid: 'toc-see-also' },
]

export default function Toc() {
  return (
    <aside className="toc" aria-label="In this article">
      <div className="toc-inner">
        <p className="toc-title">In this article</p>
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <a href={`#${item.id}`} data-testid={item.testid}>
                {item.label}
              </a>
            </li>
          ))}
        </ul>
        <div className="toc-ad" aria-hidden="true">
          <span className="ad-label">Ad</span>
          <p className="ad-title">Identity bottlenecks for AI agents</p>
          <p className="ad-body">
            Add fine-grained authorization to your app in minutes.
          </p>
          <span className="ad-btn">Start building</span>
        </div>
      </div>
    </aside>
  )
}

===FILE: src/components/Toc.css===
.toc {
  border-left: 1px solid var(--border);
}

.toc-inner {
  position: sticky;
  top: 64px;
  max-height: calc(100vh - 64px);
  overflow-y: auto;
  padding: 1.5rem 1rem 2rem;
}

.toc-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
  margin: 0 0 0.75rem;
}

.toc ul {
  list-style: none;
  margin: 0;
  padding: 0;
  border-left: 1px solid var(--border);
}

.toc li a {
  display: block;
  padding: 0.3rem 0.75rem;
  font-size: 0.8125rem;
  color: var(--text-secondary);
  border-left: 2px solid transparent;
  margin-left: -1px;
}

.toc li a:hover {
  color: var(--link);
  text-decoration: none;
  border-left-color: var(--border-strong);
}

.toc-ad {
  margin-top: 1.5rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.9rem;
  background: var(--bg-secondary);
}

.ad-label {
  font-size: 0.6875rem;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.ad-title {
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0.4rem 0;
}

.ad-body {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin: 0 0 0.6rem;
}

.ad-btn {
  display: inline-block;
  background: rgb(0, 0, 0);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.35rem 0.7rem;
  border-radius: 4px;
}

@media (max-width: 1100px) {
  .toc {
    display: none;
  }
}

===FILE: src/components/Article.tsx===
import './Article.css'
import TryIt from './TryIt'

export default function Article() {
  return (
    <article className="article">
      <h1 className="page-title">
        <code>&lt;a&gt;</code>: The Anchor element
      </h1>

      <div className="baseline">
        <span className="baseline-icon" aria-hidden="true">✓</span>
        <span className="baseline-label">Baseline</span>
        <span className="baseline-status">Widely available</span>
      </div>

      <p>
        The <code>&lt;a&gt;</code>{' '}
        <a href="/en-US/docs/Web/HTML">HTML</a> element (or{' '}
        <em>anchor</em> element), with its{' '}
        <a href="#href">
          <code>href</code>
        </a>{' '}
        attribute, creates a hyperlink to web pages, files, email addresses,
        locations in the same page, or anything else a URL can address.
      </p>

      <p>
        Content within each <code>&lt;a&gt;</code>{' '}
        <strong>should</strong> indicate the link's destination. If the{' '}
        <code>href</code> attribute is present, pressing the enter key while
        focused on the <code>&lt;a&gt;</code> element will activate it.
      </p>

      <h2 id="try_it">Try it</h2>
      <TryIt />

      <h2 id="attributes">Attributes</h2>
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
          <code>Attribution-Reporting-Eligible</code> header. On the server-side
          this is used to trigger sending an{' '}
          <code>Attribution-Reporting-Register-Source</code> header in the
          response, to register a source for attribution reporting.
        </dd>

        <dt id="download">
          <a href="#download" data-testid="content-attr-download">
            <code>download</code>
          </a>
        </dt>
        <dd>
          Causes the browser to treat the linked URL as a download. Can be used
          with or without a <code>filename</code> value. Filesystems may forbid
          certain characters in filenames, so browsers will adjust the suggested
          name if needed.
        </dd>

        <dt id="href">
          <a href="#href">
            <code>href</code>
          </a>
        </dt>
        <dd>
          The URL that the hyperlink points to. Links are not restricted to
          HTTP-based URLs &mdash; they can use any URL scheme supported by
          browsers, such as <code>tel:</code>, <code>mailto:</code>, and{' '}
          <code>sms:</code> URLs.
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
          will send <code>POST</code> requests with the body{' '}
          <code>PING</code> to the URLs. Typically used for tracking.
        </dd>

        <dt id="referrerpolicy">
          <a href="#referrerpolicy">
            <code>referrerpolicy</code>
          </a>
        </dt>
        <dd>
          How much of the referrer to send when following the link.
        </dd>

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
          tab, window, or <code>&lt;iframe&gt;</code>). Keywords include{' '}
          <code>_self</code>, <code>_blank</code>, <code>_parent</code>, and{' '}
          <code>_top</code>.
        </dd>
      </dl>

      <div className="notecard note">
        <p>
          <strong>Note:</strong> Specifying multiple URLs in some attributes
          means multiple attribution sources can be registered on the same
          feature.
        </p>
      </div>

      <h2 id="accessibility">Accessibility</h2>
      <h3>Strong link text</h3>
      <p>
        The content inside a link should indicate where the link goes, even out
        of context. Screen reader users may browse a page by listing the links,
        so link text like "click here" provides no information.
      </p>
      <pre className="code-block">
        <code>{`<a href="/en-US/docs/Web/HTML">
  Read more about HTML elements.
</a>`}</code>
      </pre>

      <h2 id="examples">Examples</h2>
      <h3>Linking to an absolute URL</h3>
      <pre className="code-block">
        <code>{`<a href="https://www.mozilla.com">Mozilla</a>`}</code>
      </pre>
      <h3>Linking to relative URLs</h3>
      <pre className="code-block">
        <code>{`<a href="//example.com">Scheme-relative URL</a>
<a href="/en-US/docs/Web/HTML">Origin-relative URL</a>
<a href="p">Directory-relative URL</a>`}</code>
      </pre>
      <h3>Linking to an email address</h3>
      <pre className="code-block">
        <code>{`<a href="mailto:nowhere@mozilla.org">Send email to nowhere</a>`}</code>
      </pre>

      <h2 id="security_and_privacy">Security and privacy</h2>
      <p>
        <code>&lt;a&gt;</code> elements can have consequences for users' security
        and privacy. When using <code>target="_blank"</code> without{' '}
        <code>rel="noopener"</code>, the new page can access your{' '}
        <code>window.opener</code> object, which may allow phishing attacks. Use{' '}
        <code>rel="noreferrer"</code> to avoid leaking referrer information.
      </p>

      <h2 id="technical_summary">Technical summary</h2>
      <div className="table-wrap">
        <table className="prop-table">
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
              <td>None, both the starting and ending tags are mandatory.</td>
            </tr>
            <tr>
              <th scope="row">Permitted parents</th>
              <td>Any element that accepts phrasing content, or any flow content.</td>
            </tr>
            <tr>
              <th scope="row">Implicit ARIA role</th>
              <td>
                <code>link</code> when <code>href</code> is present, otherwise{' '}
                <code>generic</code>
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
      </div>

      <h2 id="specifications">Specifications</h2>
      <div className="table-wrap">
        <table className="prop-table">
          <thead>
            <tr>
              <th scope="col">Specification</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                HTML
                <br />
                <code># the-a-element</code>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 id="browser_compatibility">Browser compatibility</h2>
      <div className="table-wrap">
        <table className="prop-table compat">
          <thead>
            <tr>
              <th scope="col">Feature</th>
              <th scope="col">Chrome</th>
              <th scope="col">Edge</th>
              <th scope="col">Firefox</th>
              <th scope="col">Safari</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">
                <code>a</code>
              </th>
              <td className="yes">1</td>
              <td className="yes">12</td>
              <td className="yes">1</td>
              <td className="yes">1</td>
            </tr>
            <tr>
              <th scope="row">
                <code>download</code>
              </th>
              <td className="yes">14</td>
              <td className="yes">18</td>
              <td className="yes">20</td>
              <td className="yes">10.1</td>
            </tr>
            <tr>
              <th scope="row">
                <code>href</code>
              </th>
              <td className="yes">1</td>
              <td className="yes">12</td>
              <td className="yes">1</td>
              <td className="yes">1</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 id="see_also">See also</h2>
      <ul className="see-also">
        <li>
          <a href="/en-US/docs/Learn/HTML/Introduction_to_HTML/Creating_hyperlinks">
            Creating hyperlinks
          </a>
        </li>
        <li>
          <a href="/en-US/docs/Web/HTTP/Headers/Content-Disposition">
            <code>Content-Disposition</code> header
          </a>
        </li>
        <li>
          <a href="/en-US/docs/Web/API/HTMLAnchorElement">
            <code>HTMLAnchorElement</code>
          </a>
        </li>
      </ul>
    </article>
  )
}

===FILE: src/components/Article.css===
.article {
  font-size: 1rem;
  color: var(--text);
  max-width: 760px;
}

.page-title {
  font-size: 2rem;
  font-weight: 600;
  margin: 0.75rem 0 1rem;
  line-height: 1.2;
}

.page-title code {
  font-size: 0.9em;
  background: var(--code-bg);
  padding: 0.05em 0.3em;
  border-radius: 4px;
}

.article p {
  margin: 1rem 0;
}

.article h2 {
  font-size: 1.75rem;
  margin: 2.25rem 0 1rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
}

.article h3 {
  font-size: 1.25rem;
  margin: 1.75rem 0 0.75rem;
}

.article code {
  background: var(--code-bg);
  padding: 0.1em 0.35em;
  border-radius: 4px;
  color: rgb(43, 43, 43);
}

.baseline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--green-bg);
  border: 1px solid var(--green-bg-light);
  border-radius: 6px;
  padding: 0.6rem 0.9rem;
  font-size: 0.875rem;
  margin: 1rem 0 1.5rem;
}

.baseline-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  background: rgb(30, 134, 87);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
}

.baseline-label {
  font-weight: 700;
}

.baseline-status {
  color: var(--text-secondary);
}

.attr-list {
  margin: 1rem 0;
}

.attr-list dt {
  margin-top: 1.25rem;
  font-weight: 500;
}

.attr-list dt code {
  background: var(--code-bg);
}

.attr-list dd {
  margin: 0.4rem 0 0;
  color: var(--text);
}

.badge {
  display: inline-block;
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  vertical-align: middle;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.badge.experimental {
  background: rgb(236, 244, 254);
  color: var(--link);
  border: 1px solid rgb(193, 219, 251);
}

.notecard {
  border-radius: 6px;
  padding: 0.75rem 1rem;
  margin: 1.25rem 0;
  font-size: 0.9375rem;
  border-left: 4px solid;
}

.notecard.note {
  background: var(--note-bg);
  border-left-color: var(--link);
}

.notecard p {
  margin: 0;
}

.code-block {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
  font-family: var(--mono);
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 1rem 0;
}

.code-block code {
  background: transparent;
  padding: 0;
  color: rgb(43, 43, 43);
  white-space: pre;
}

.table-wrap {
  overflow-x: auto;
  margin: 1rem 0;
}

.prop-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.prop-table th,
.prop-table td {
  border: 1px solid var(--border);
  padding: 0.55rem 0.75rem;
  text-align: left;
  vertical-align: top;
}

.prop-table th[scope='row'] {
  background: var(--bg-secondary);
  font-weight: 600;
  white-space: nowrap;
}

.prop-table thead th {
  background: var(--bg-secondary);
}

.prop-table.compat td {
  text-align: center;
}

.prop-table.compat td.yes {
  background: var(--green-bg);
  color: rgb(30, 110, 70);
  font-weight: 600;
}

.see-also {
  margin: 1rem 0;
  padding-left: 1.25rem;
}

.see-also li {
  margin: 0.35rem 0;
}

===FILE: src/components/TryIt.tsx===
import { useState } from 'react'
import './TryIt.css'

const htmlCode = `<p>You can reach Michael at:</p>

<ul>
  <li><a href="https://example.com">Website</a></li>
  <li><a href="mailto:m.bluth@example.com">Email</a></li>
  <li><a href="tel:+123456789">Phone</a></li>
</ul>`

const cssCode = `li {
  margin-bottom: 0.5rem;
}`

export default function TryIt() {
  const [tab, setTab] = useState<'html' | 'css'>('html')

  return (
    <div className="try-it">
      <p className="try-it-label">HTML Demo: &lt;a&gt;</p>
      <div className="try-it-panes">
        <div className="editor">
          <div className="editor-tabs">
            <button
              type="button"
              className={tab === 'html' ? 'tab active' : 'tab'}
              onClick={() => setTab('html')}
            >
              HTML
            </button>
            <button
              type="button"
              className={tab === 'css' ? 'tab active' : 'tab'}
              onClick={() => setTab('css')}
            >
              CSS
            </button>
            <button type="button" className="reset-btn">
              Reset
            </button>
          </div>
          <pre className="editor-code">
            <code>{tab === 'html' ? htmlCode : cssCode}</code>
          </pre>
        </div>

        <div className="output">
          <div className="output-header">OUTPUT</div>
          <div className="output-body">
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
    </div>
  )
}

===FILE: src/components/TryIt.css===
.try-it {
  margin: 1rem 0 2rem;
}

.try-it-label {
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  color: var(--text-secondary);
}

.try-it-panes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
}

.editor {
  border-right: 1px solid var(--border);
  background: var(--code-bg);
  min-width: 0;
}

.editor-tabs {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.4rem 0.5rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}

.tab {
  background: transparent;
  border: none;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-secondary);
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  cursor: pointer;
}

.tab.active {
  background: var(--code-bg);
  color: var(--text);
}

.reset-btn {
  margin-left: auto;
  background: transparent;
  border: 1px solid var(--border-strong);
  font-family: inherit;
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  cursor: pointer;
  color: var(--text);
}

.editor-code {
  margin: 0;
  padding: 0.85rem;
  font-family: var(--mono);
  font-size: 0.8rem;
  line-height: 1.5;
  overflow-x: auto;
}

.editor-code code {
  background: transparent;
  white-space: pre;
  color: rgb(43, 43, 43);
}

.output {
  background: var(--bg);
  min-width: 0;
}

.output-header {
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
  padding: 0.5rem 0.85rem;
  border-bottom: 1px solid var(--border);
}

.output-body {
  padding: 0.85rem;
  font-size: 0.9375rem;
}

.output-body p {
  margin: 0 0 0.5rem;
}

.output-body ul {
  margin: 0;
  padding-left: 1.2rem;
}

.output-body li {
  margin-bottom: 0.4rem;
}

@media (max-width: 600px) {
  .try-it-panes {
    grid-template-columns: 1fr;
  }
  .editor {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
}