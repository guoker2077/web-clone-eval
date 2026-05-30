===FILE: package.json===
{
  "name": "bing-replica",
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
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}

===FILE: index.html===
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>必应</title>
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
  </StrictMode>
)

===FILE: src/index.css===
* {
  box-sizing: border-box;
}

html,
body,
#root {
  margin: 0;
  padding: 0;
}

body {
  font-family: "Segoe UI", Segoe, Tahoma, Arial, Verdana, sans-serif;
  color: rgb(17, 17, 17);
  background: #fff;
}

a {
  text-decoration: none;
  cursor: pointer;
  color: inherit;
}

button {
  font-family: inherit;
}

===FILE: src/data/mockSearch.ts===
export interface SearchResult {
  title: string
  url: string
  displayUrl: string
  snippet: string
}

export const TOTAL_PAGES = 10
export const PER_PAGE = 10

const SOURCES = [
  'zhihu.com',
  'baike.baidu.com',
  'wikipedia.org',
  'news.sina.com.cn',
  'weibo.com',
  'bilibili.com',
  'github.com',
  'csdn.net',
  'cnblogs.com',
  '36kr.com',
]

export function getResults(query: string, page: number): SearchResult[] {
  const results: SearchResult[] = []
  for (let i = 0; i < PER_PAGE; i++) {
    const n = (page - 1) * PER_PAGE + i + 1
    const host = SOURCES[(n - 1) % SOURCES.length]
    results.push({
      title: `${query} - 详细介绍与相关资讯（结果 ${n}）`,
      url: `https://${host}/search?q=${encodeURIComponent(query)}&n=${n}`,
      displayUrl: `${host} › ${encodeURIComponent(query)} › 第${n}条`,
      snippet: `关于"${query}"的搜索结果 ${n}：这里汇总了与 ${query} 相关的最新内容、背景介绍、使用方法与常见问题，帮助你快速、全面地了解 ${query} 的更多信息和延伸阅读。`,
    })
  }
  return results
}

export function getResultCount(query: string): string {
  const base = (query.length + 3) * 1837461
  return base.toLocaleString('en-US')
}

===FILE: src/components/SearchBox.tsx===
import type { ChangeEvent, FormEvent } from 'react'
import './SearchBox.css'

interface Props {
  value: string
  onChange: (v: string) => void
  onSearch: (v: string) => void
  variant?: 'home' | 'results'
}

export default function SearchBox({ value, onChange, onSearch, variant = 'home' }: Props) {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onSearch(value)
  }

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value)
  }

  return (
    <form
      className={`sb_form sb_${variant}`}
      onSubmit={handleSubmit}
      role="search"
      action="#"
    >
      <input
        id="sb_form_q"
        name="q"
        data-testid="search-input"
        className="sb_input"
        type="text"
        value={value}
        onChange={handleChange}
        autoComplete="off"
        aria-label="搜索"
        placeholder=""
      />

      <span className="sb_mic" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18">
          <path
            fill="currentColor"
            d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V22h2v-3.08A7 7 0 0 0 19 12h-2z"
          />
        </svg>
      </span>

      <button
        id="sb_form_go"
        data-testid="search-button"
        className="sb_go"
        type="submit"
        aria-label="搜索"
      >
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path
            fill="currentColor"
            d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.49 4.49 0 0 1 9.5 14z"
          />
        </svg>
      </button>
    </form>
  )
}

===FILE: src/components/SearchBox.css===
.sb_form {
  display: flex;
  align-items: center;
  background: #fff;
}

/* ---- Home variant ---- */
.sb_form.sb_home {
  width: 500px;
  max-width: 92vw;
  height: 48px;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.sb_home .sb_input {
  flex: 1;
  height: 100%;
  border: none;
  outline: none;
  padding: 0 18px;
  font-size: 16px;
  color: rgb(17, 17, 17);
  background: transparent;
}

.sb_home .sb_mic {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 100%;
  color: #4c4c4c;
  cursor: pointer;
}

.sb_home .sb_go {
  width: 56px;
  height: 100%;
  border: none;
  border-left: 1px solid #ececec;
  background: #fff;
  color: #4c4c4c;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.sb_home .sb_go:hover {
  color: #0067b8;
}

/* ---- Results variant ---- */
.sb_form.sb_results {
  width: 480px;
  max-width: 60vw;
  height: 40px;
  border: 1px solid #ddd;
  border-radius: 22px;
  padding-left: 18px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.sb_results .sb_input {
  flex: 1;
  height: 100%;
  border: none;
  outline: none;
  font-size: 15px;
  color: rgb(17, 17, 17);
  background: transparent;
}

.sb_results .sb_mic {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 100%;
  color: #4c4c4c;
}

.sb_results .sb_go {
  width: 46px;
  height: 100%;
  border: none;
  background: transparent;
  color: #0067b8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 0 22px 22px 0;
}

.sb_results .sb_go:hover {
  background: #f3f3f3;
}

===FILE: src/components/HomePage.tsx===
import SearchBox from './SearchBox'
import './HomePage.css'

interface Props {
  query: string
  setQuery: (q: string) => void
  onSearch: (q: string) => void
}

const navLinks = ['图片', '视频', '翻译', '地图', '学术', '···']

const heroNews = [
  { title: '诺基亚发布首款微聊手机', color: 'linear-gradient(135deg,#3a4a5a,#6b7b8b)' },
  { title: '九寨沟照镜子被索要2元？', color: 'linear-gradient(135deg,#2f6b4f,#5aa07a)' },
  { title: '比亚迪发布超级智能体迪迪虾', color: 'linear-gradient(135deg,#1a1a1a,#444)' },
  { title: '英伟达黄仁勋评价韬定律', color: 'linear-gradient(135deg,#243b53,#456)' },
  { title: '必应学术搜索火热上新', color: 'linear-gradient(135deg,#0a5a8a,#2b8ccc)' },
]

const cards = [
  { src: '华声在线', time: '2 天', title: '肝不好，头先知！这些头部信号一出现，立即检查别拖延！', color: 'linear-gradient(135deg,#d8c3a5,#b89b7c)' },
  { src: '博禾医生', time: '3 千', title: '一周至少15次!52岁男子肾衰竭，妻子：劝了很多次，就是不听', color: 'linear-gradient(135deg,#e8d5c0,#caa982)' },
  { src: '一点资讯', time: '19 小时', title: '相差六岁，姐弟恋，领证七年生下两个孩子后才举行婚礼', color: 'linear-gradient(135deg,#c0392b,#e57373)' },
  { src: '华声在线', time: '1 天', title: '长肉巨快的5种食物，面条只排第二，第一名很多人没想到', color: 'linear-gradient(135deg,#f0c14b,#e6a817)' },
  { src: '光影新视界', time: '3 天', title: '刘浩存拍完主角后不敢去孙浩家 原来是怕进门先背台词', color: 'linear-gradient(135deg,#5a4a6a,#8a6a9a)' },
  { src: '一点资讯', time: '视频', title: '熊猫团子躲在墙角生闷气，饲养员安慰不料反被打', color: 'linear-gradient(135deg,#4a5a6a,#7a8a9a)' },
  { src: '人民网', time: '7 小时', title: '神舟二十二号载人飞船返回舱成功着陆', color: 'linear-gradient(135deg,#c0392b,#d35400)' },
  { src: 'ZAKER娱乐', time: '1 天', title: '女演员长相有多重要？43岁高露给小14岁李昀锐演妈', color: 'linear-gradient(135deg,#6a8a5a,#9ab87a)' },
  { src: '一点资讯', time: '17 小时', title: '曾因言论翻车今又惹怒跑男粉，白鹿一月掉粉百万', color: 'linear-gradient(135deg,#8a5a6a,#b87a8a)' },
]

export default function HomePage({ query, setQuery, onSearch }: Props) {
  return (
    <div className="home">
      <header className="bing-nav">
        <div className="nav-left">
          <span className="ms-logo">
            <span className="ms-grid">
              <i style={{ background: '#f25022' }} />
              <i style={{ background: '#7fba00' }} />
              <i style={{ background: '#00a4ef' }} />
              <i style={{ background: '#ffb900' }} />
            </span>
            <span className="ms-text">Microsoft Bing</span>
          </span>
          <nav className="nav-links">
            {navLinks.map((l) => (
              <a key={l}>{l}</a>
            ))}
          </nav>
        </div>
        <div className="nav-right">
          <a className="nav-pill">登录 <span className="dot avatar" /></a>
          <a className="nav-pill">Rewards <span className="dot reward" /></a>
          <a className="nav-pill">手机版 <span className="dot phone" /></a>
          <button className="hamburger" aria-label="菜单">≡</button>
        </div>
      </header>

      <section className="hero">
        <svg
          className="mountains"
          viewBox="0 0 1440 620"
          preserveAspectRatio="xMidYMid slice"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#0f2c47" />
              <stop offset="55%" stopColor="#3d7099" />
              <stop offset="100%" stopColor="#7aa9c9" />
            </linearGradient>
            <linearGradient id="peak" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f7c97a" />
              <stop offset="35%" stopColor="#e89a4f" />
              <stop offset="100%" stopColor="#566472" />
            </linearGradient>
          </defs>
          <rect width="1440" height="620" fill="url(#sky)" />
          <polygon
            points="0,620 0,430 250,310 480,410 700,270 920,420 1180,300 1440,440 1440,620"
            fill="#2f4a5e"
            opacity="0.55"
          />
          <polygon points="560,620 980,150 1440,620" fill="url(#peak)" />
          <polygon points="900,300 980,150 1062,300 980,250" fill="#ffffff" opacity="0.85" />
          <polygon
            points="0,620 360,360 720,520 1100,380 1440,560 1440,620"
            fill="#335a6e"
          />
        </svg>

        <div className="search-wrap">
          <SearchBox value={query} onChange={setQuery} onSearch={onSearch} variant="home" />
        </div>

        <div className="hero-news">
          {heroNews.map((n, i) => (
            <article className="hero-card" key={i}>
              <div className="hero-card-img" style={{ background: n.color }} />
              <span className="hero-card-title">{n.title}</span>
            </article>
          ))}
        </div>
      </section>

      <main className="discover">
        <h2 className="discover-title">发现</h2>
        <div className="cards">
          {cards.map((c, i) => (
            <article className="card" key={i}>
              <div className="card-img" style={{ background: c.color }} />
              <div className="card-meta">
                {c.src} · {c.time}
              </div>
              <h3 className="card-title">{c.title}</h3>
            </article>
          ))}
        </div>
      </main>
    </div>
  )
}

===FILE: src/components/HomePage.css===
.home {
  min-height: 100vh;
  background: rgb(236, 236, 236);
}

/* ---------- Nav ---------- */
.bing-nav {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 10;
  color: #fff;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 28px;
}

.ms-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 19px;
  font-weight: 600;
  color: #fff;
}

.ms-grid {
  display: grid;
  grid-template-columns: 9px 9px;
  grid-template-rows: 9px 9px;
  gap: 2px;
}

.ms-grid i {
  display: block;
  width: 9px;
  height: 9px;
}

.nav-links {
  display: flex;
  gap: 20px;
  font-size: 14px;
}

.nav-links a {
  color: rgba(255, 255, 255, 0.92);
}

.nav-links a:hover {
  text-decoration: underline;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 14px;
}

.nav-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: rgba(255, 255, 255, 0.92);
}

.dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: inline-block;
}

.dot.avatar {
  background: rgba(255, 255, 255, 0.85);
}

.dot.reward {
  background: #f7b500;
}

.dot.phone {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  width: 14px;
  height: 18px;
}

.hamburger {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 22px;
  cursor: pointer;
  line-height: 1;
}

/* ---------- Hero ---------- */
.hero {
  position: relative;
  height: 620px;
  overflow: hidden;
}

.mountains {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.search-wrap {
  position: relative;
  z-index: 5;
  display: flex;
  justify-content: center;
  padding-top: 132px;
}

.hero-news {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 5;
  display: flex;
  gap: 2px;
  padding: 12px 0 0;
}

.hero-card {
  flex: 1;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(2px);
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 96px;
}

.hero-card-title {
  color: rgba(255, 255, 255, 0.95);
  font-size: 13px;
  line-height: 1.4;
}

.hero-card-img {
  width: 100%;
  height: 44px;
  border-radius: 3px;
}

/* ---------- Discover feed ---------- */
.discover {
  max-width: 1130px;
  margin: 0 auto;
  padding: 24px 16px 60px;
}

.discover-title {
  font-size: 16px;
  font-weight: 600;
  color: rgb(34, 34, 34);
  margin: 0 0 16px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding-bottom: 14px;
}

.card-img {
  width: 100%;
  height: 168px;
}

.card-meta {
  font-size: 12.8px;
  color: #767676;
  padding: 10px 14px 4px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: rgb(34, 34, 34);
  line-height: 1.45;
  margin: 0;
  padding: 0 14px;
}

@media (max-width: 820px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
  .nav-links {
    display: none;
  }
}

@media (max-width: 540px) {
  .cards {
    grid-template-columns: 1fr;
  }
}

===FILE: src/components/ResultsPage.tsx===
import SearchBox from './SearchBox'
import { getResults, getResultCount, TOTAL_PAGES } from '../data/mockSearch'
import './ResultsPage.css'

interface Props {
  query: string
  setQuery: (q: string) => void
  submitted: string
  page: number
  setPage: (p: number) => void
  onSearch: (q: string) => void
  onHome: () => void
}

const tabs = ['全部', '图片', '视频', '地图', '资讯', '更多']

export default function ResultsPage({
  query,
  setQuery,
  submitted,
  page,
  setPage,
  onSearch,
  onHome,
}: Props) {
  const results = getResults(submitted, page)

  const changePage = (p: number) => {
    if (p < 1 || p > TOTAL_PAGES) return
    setPage(p)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const pageNumbers = Array.from({ length: TOTAL_PAGES }, (_, i) => i + 1)

  return (
    <div className="results-page">
      <header className="results-header">
        <div className="results-header-top">
          <span className="results-logo" onClick={onHome}>
            <span className="ms-grid-sm">
              <i style={{ background: '#f25022' }} />
              <i style={{ background: '#7fba00' }} />
              <i style={{ background: '#00a4ef' }} />
              <i style={{ background: '#ffb900' }} />
            </span>
            <b>Microsoft Bing</b>
          </span>
          <SearchBox value={query} onChange={setQuery} onSearch={onSearch} variant="results" />
        </div>
        <nav className="results-tabs">
          {tabs.map((t, i) => (
            <a key={t} className={i === 0 ? 'active' : ''}>
              {t}
            </a>
          ))}
        </nav>
      </header>

      <main className="results-body" data-testid="search-results">
        <div className="results-count">
          约 {getResultCount(submitted)} 条结果（第 {page} 页）
        </div>

        <ol id="b_results" data-testid="result-list">
          {results.map((r, i) => (
            <li className="b_algo" key={`${page}-${i}`}>
              <div className="b_url">{r.displayUrl}</div>
              <h2 className="b_title">
                <a href={r.url} onClick={(e) => e.preventDefault()}>
                  {r.title}
                </a>
              </h2>
              <p className="b_caption">{r.snippet}</p>
            </li>
          ))}
        </ol>

        <nav className="b_pag" aria-label="分页">
          {page > 1 && (
            <a
              className="sb_pagP"
              role="button"
              title="上一页"
              aria-label="上一页"
              onClick={() => changePage(page - 1)}
            >
              ‹ 上一页
            </a>
          )}

          {pageNumbers.map((p) => (
            <a
              key={p}
              className={p === page ? 'pag_num pag_cur' : 'pag_num'}
              role="button"
              onClick={() => changePage(p)}
            >
              {p}
            </a>
          ))}

          <a
            className="sb_pagN"
            data-testid="next-page"
            role="button"
            title="下一页"
            aria-label="下一页"
            onClick={() => changePage(page + 1)}
          >
            下一页 ›
          </a>
        </nav>
      </main>
    </div>
  )
}

===FILE: src/components/ResultsPage.css===
.results-page {
  min-height: 100vh;
  background: #fff;
  color: rgb(17, 17, 17);
}

/* ---------- Header ---------- */
.results-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: #fff;
  border-bottom: 1px solid #ddd;
}

.results-header-top {
  display: flex;
  align-items: center;
  gap: 28px;
  padding: 14px 24px 10px;
}

.results-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  color: rgb(17, 17, 17);
  cursor: pointer;
  white-space: nowrap;
}

.results-logo b {
  font-weight: 600;
}

.ms-grid-sm {
  display: grid;
  grid-template-columns: 8px 8px;
  grid-template-rows: 8px 8px;
  gap: 2px;
}

.ms-grid-sm i {
  display: block;
  width: 8px;
  height: 8px;
}

.results-tabs {
  display: flex;
  gap: 26px;
  padding: 0 24px;
  margin-left: 0;
}

.results-tabs a {
  padding: 8px 0 12px;
  font-size: 14px;
  color: #767676;
  border-bottom: 3px solid transparent;
}

.results-tabs a:hover {
  color: rgb(17, 17, 17);
}

.results-tabs a.active {
  color: rgb(17, 17, 17);
  font-weight: 600;
  border-bottom-color: #0067b8;
}

/* ---------- Body ---------- */
.results-body {
  max-width: 1000px;
  padding: 22px 24px 60px;
}

.results-count {
  font-size: 13px;
  color: #767676;
  margin-bottom: 18px;
}

#b_results {
  list-style: none;
  margin: 0;
  padding: 0;
  max-width: 640px;
}

.b_algo {
  margin-bottom: 26px;
}

.b_url {
  font-size: 13px;
  color: #0e7b1f;
  margin-bottom: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.b_title {
  margin: 0 0 4px;
  font-size: 19px;
  font-weight: 400;
  line-height: 1.3;
}

.b_title a {
  color: #1a0dab;
}

.b_title a:hover {
  text-decoration: underline;
}

.b_caption {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: rgb(76, 76, 76);
}

/* ---------- Pagination ---------- */
.b_pag {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  max-width: 640px;
}

.b_pag a {
  min-width: 32px;
  height: 32px;
  padding: 0 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #0067b8;
  border-radius: 4px;
}

.b_pag a:hover {
  background: #f0f0f0;
}

.pag_cur {
  color: rgb(17, 17, 17) !important;
  font-weight: 700;
  background: #ececec;
}

.sb_pagN,
.sb_pagP {
  font-weight: 600;
}

@media (max-width: 720px) {
  .sb_form.sb_results {
    width: 100%;
    max-width: none;
  }
  .results-header-top {
    flex-wrap: wrap;
    gap: 12px;
  }
}

===FILE: src/App.tsx===
import { useState } from 'react'
import HomePage from './components/HomePage'
import ResultsPage from './components/ResultsPage'

export default function App() {
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [page, setPage] = useState(1)
  const [view, setView] = useState<'home' | 'results'>('home')

  const handleSearch = (q: string) => {
    const trimmed = q.trim()
    if (!trimmed) return
    setQuery(trimmed)
    setSubmitted(trimmed)
    setPage(1)
    setView('results')
  }

  const goHome = () => {
    setView('home')
  }

  if (view === 'home') {
    return <HomePage query={query} setQuery={setQuery} onSearch={handleSearch} />
  }

  return (
    <ResultsPage
      query={query}
      setQuery={setQuery}
      submitted={submitted}
      page={page}
      setPage={setPage}
      onSearch={handleSearch}
      onHome={goHome}
    />
  )
}