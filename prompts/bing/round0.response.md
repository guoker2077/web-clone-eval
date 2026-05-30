===FILE: package.json===
{
  "name": "bing-clone",
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
  "include": ["src"]
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
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  font-family: 'Segoe UI', Segoe, Tahoma, Arial, Verdana, sans-serif;
  color: rgb(17, 17, 17);
  background: rgb(255, 255, 255);
  -webkit-font-smoothing: antialiased;
}

a {
  text-decoration: none;
  color: inherit;
}

ol,
ul {
  list-style: none;
}

button {
  font-family: inherit;
  cursor: pointer;
}

input {
  font-family: inherit;
}

===FILE: src/App.tsx===
import { useState } from 'react'
import Header from './components/Header'
import Hero from './components/Hero'
import SearchResults from './components/SearchResults'
import { search } from './data/mockData'
import type { SearchResult } from './data/mockData'
import './App.css'

const PAGE_SIZE = 8

export default function App() {
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [page, setPage] = useState(1)
  const [results, setResults] = useState<SearchResult[]>([])
  const [total, setTotal] = useState(0)

  const runSearch = (term: string, pageNum: number) => {
    const keyword = term.trim()
    if (!keyword) return
    const { items, total } = search(keyword, pageNum, PAGE_SIZE)
    setResults(items)
    setTotal(total)
    setSubmitted(keyword)
    setPage(pageNum)
  }

  const handleSearch = (term: string) => {
    runSearch(term, 1)
  }

  const handleNextPage = () => {
    runSearch(submitted, page + 1)
  }

  const handlePrevPage = () => {
    if (page > 1) runSearch(submitted, page - 1)
  }

  const hasResults = submitted !== ''
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE))

  return (
    <div className="app">
      <Header
        compact={hasResults}
        query={query}
        onQueryChange={setQuery}
        onSearch={handleSearch}
      />
      {hasResults ? (
        <SearchResults
          keyword={submitted}
          results={results}
          total={total}
          page={page}
          totalPages={totalPages}
          onNextPage={handleNextPage}
          onPrevPage={handlePrevPage}
        />
      ) : (
        <Hero
          query={query}
          onQueryChange={setQuery}
          onSearch={handleSearch}
        />
      )}
    </div>
  )
}

===FILE: src/App.css===
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

===FILE: src/components/Header.tsx===
import SearchBar from './SearchBar'
import './Header.css'

interface HeaderProps {
  compact: boolean
  query: string
  onQueryChange: (value: string) => void
  onSearch: (term: string) => void
}

const navItems = ['图片', '视频', '翻译', '地图', '学术', '···']

export default function Header({ compact, query, onQueryChange, onSearch }: HeaderProps) {
  return (
    <header className={compact ? 'header header--compact' : 'header'}>
      <div className="header__inner">
        <a className="header__logo" href="#">
          <span className="header__logo-mark" aria-hidden="true" />
          <span className="header__logo-text">
            Microsoft <strong>Bing</strong>
          </span>
        </a>

        {compact && (
          <div className="header__search">
            <SearchBar
              compact
              query={query}
              onQueryChange={onQueryChange}
              onSearch={onSearch}
            />
          </div>
        )}

        <nav className="header__nav">
          {navItems.map((item) => (
            <a key={item} className="header__nav-item" href="#">
              {item}
            </a>
          ))}
        </nav>

        <div className="header__actions">
          <a className="header__action" href="#">
            登录 <span className="header__avatar" aria-hidden="true" />
          </a>
          <a className="header__action header__action--rewards" href="#">
            Rewards <span className="header__rewards" aria-hidden="true" />
          </a>
          <span className="header__icon header__icon--mobile" aria-hidden="true" />
          <span className="header__icon header__icon--menu" aria-hidden="true" />
        </div>
      </div>
    </header>
  )
}

===FILE: src/components/Header.css===
.header {
  position: relative;
  z-index: 5;
  width: 100%;
}

.header__inner {
  display: flex;
  align-items: center;
  height: 56px;
  padding: 0 24px;
  gap: 22px;
  color: rgb(255, 255, 255);
}

.header__logo {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.header__logo-mark {
  width: 22px;
  height: 22px;
  background: linear-gradient(135deg, #f25022 0 50%, #7fba00 0 100%);
  background:
    linear-gradient(#f25022, #f25022) 0 0 / 10px 10px no-repeat,
    linear-gradient(#7fba00, #7fba00) 12px 0 / 10px 10px no-repeat,
    linear-gradient(#00a4ef, #00a4ef) 0 12px / 10px 10px no-repeat,
    linear-gradient(#ffb900, #ffb900) 12px 12px / 10px 10px no-repeat;
}

.header__logo-text {
  font-size: 21px;
  font-weight: 400;
  letter-spacing: 0.2px;
}

.header__logo-text strong {
  font-weight: 600;
}

.header__nav {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-shrink: 0;
}

.header__nav-item {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  white-space: nowrap;
}

.header__nav-item:hover {
  color: #fff;
}

.header__search {
  flex: 1;
  max-width: 460px;
}

.header__actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 18px;
  flex-shrink: 0;
}

.header__action {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.95);
  white-space: nowrap;
}

.header__avatar {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.85);
  display: inline-block;
}

.header__rewards {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #6cb33f;
  display: inline-block;
}

.header__icon {
  width: 22px;
  height: 22px;
  display: inline-block;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 3px;
}

.header__icon--mobile {
  width: 16px;
  height: 22px;
  border-radius: 3px;
}

/* Compact header used on results page */
.header--compact {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.header--compact .header__inner {
  color: rgb(17, 17, 17);
  height: 64px;
}

.header--compact .header__logo-text {
  color: rgb(17, 17, 17);
}

.header--compact .header__nav-item,
.header--compact .header__action {
  color: rgb(76, 76, 76);
}

.header--compact .header__avatar,
.header--compact .header__icon {
  background: rgba(0, 0, 0, 0.4);
}

@media (max-width: 860px) {
  .header__nav,
  .header__actions {
    display: none;
  }
  .header--compact .header__search {
    max-width: none;
  }
}

===FILE: src/components/SearchBar.tsx===
import { useState } from 'react'
import type { FormEvent } from 'react'
import './SearchBar.css'

interface SearchBarProps {
  compact?: boolean
  query: string
  onQueryChange: (value: string) => void
  onSearch: (term: string) => void
}

export default function SearchBar({ compact = false, query, onQueryChange, onSearch }: SearchBarProps) {
  const [focused, setFocused] = useState(false)

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onSearch(query)
  }

  return (
    <form
      id="sb_form"
      className={`searchbar${compact ? ' searchbar--compact' : ''}${focused ? ' searchbar--focused' : ''}`}
      onSubmit={handleSubmit}
      role="search"
    >
      <input
        id="sb_form_q"
        name="q"
        className="searchbar__input"
        type="text"
        autoComplete="off"
        placeholder="搜索网页"
        aria-label="输入搜索词"
        data-testid="search-input"
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
      />
      <span className="searchbar__mic" aria-hidden="true" />
      <button
        id="sb_form_go"
        className="searchbar__go"
        type="submit"
        aria-label="搜索"
        data-testid="search-button"
      >
        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
          <path
            fill="currentColor"
            d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.5 4.5 0 0 1 9.5 14z"
          />
        </svg>
      </button>
    </form>
  )
}

===FILE: src/components/SearchBar.css===
.searchbar {
  display: flex;
  align-items: center;
  width: 100%;
  height: 44px;
  background: #fff;
  border: 1px solid #d2d2d2;
  border-radius: 22px;
  padding: 0 6px 0 18px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.15s ease, border-color 0.15s ease;
}

.searchbar--focused {
  border-color: #0078d4;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16);
}

.searchbar__input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  color: rgb(17, 17, 17);
  background: transparent;
  height: 100%;
}

.searchbar__input::placeholder {
  color: #767676;
}

.searchbar__mic {
  width: 1px;
  height: 24px;
  margin: 0 14px;
  position: relative;
  background: #e0e0e0;
  flex-shrink: 0;
}

.searchbar__mic::after {
  content: '';
  position: absolute;
  left: -22px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  background:
    radial-gradient(circle at 50% 35%, #767676 0 5px, transparent 6px);
  border-radius: 2px;
}

.searchbar__go {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: #0f6cbd;
  flex-shrink: 0;
}

.searchbar__go:hover {
  background: rgba(0, 0, 0, 0.05);
}

/* Compact variant in results header */
.searchbar--compact {
  height: 40px;
  border-radius: 20px;
  box-shadow: none;
  border-color: #cfcfcf;
}

.searchbar--compact .searchbar__input {
  font-size: 14px;
}

===FILE: src/components/Hero.tsx===
import SearchBar from './SearchBar'
import './Hero.css'

interface HeroProps {
  query: string
  onQueryChange: (value: string) => void
  onSearch: (term: string) => void
}

const trending = [
  '诺基亚发布首款微聊手机',
  '九寨沟照镜子被索要2元？',
  '比亚迪发布超级智能体迪迪虾',
  '英伟达黄仁勋评价锁定律',
  '必应学术搜索火热上新',
  '电车是时候交养路费了？',
]

export default function Hero({ query, onQueryChange, onSearch }: HeroProps) {
  return (
    <main className="hero">
      <div className="hero__bg" />
      <div className="hero__overlay" />

      <div className="hero__content">
        <div className="hero__search">
          <SearchBar query={query} onQueryChange={onQueryChange} onSearch={onSearch} />
        </div>
      </div>

      <div className="hero__caption">
        <span className="hero__caption-pin" aria-hidden="true" />
        A 'peak' into history
      </div>

      <div className="hero__trending">
        <div className="hero__trending-inner">
          {trending.map((item, i) => (
            <button
              key={i}
              className="hero__trending-card"
              onClick={() => onSearch(item)}
              type="button"
            >
              <span className="hero__trending-text">{item}</span>
            </button>
          ))}
        </div>
      </div>
    </main>
  )
}

===FILE: src/components/Hero.css===
.hero {
  position: relative;
  width: 100%;
  height: 620px;
  margin-top: -56px;
  padding-top: 56px;
  overflow: hidden;
}

.hero__bg {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, #1b3a5b 0%, #2f6191 35%, #4a7fae 60%, #7fa6c4 100%);
}

.hero__bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 40% at 70% 20%, rgba(255, 184, 92, 0.55), transparent 70%),
    radial-gradient(ellipse 50% 30% at 45% 45%, rgba(255, 255, 255, 0.12), transparent 70%);
}

.hero__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.25) 0%, transparent 25%);
}

.hero__content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: center;
  padding-top: 100px;
}

.hero__search {
  width: 100%;
  max-width: 500px;
  padding: 0 16px;
}

.hero__caption {
  position: absolute;
  z-index: 2;
  right: 80px;
  bottom: 196px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(0, 0, 0, 0.35);
  color: rgba(255, 255, 255, 0.92);
  font-size: 13px;
  border-radius: 4px;
}

.hero__caption-pin {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.9);
}

.hero__trending {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  background: rgba(34, 34, 34, 0.55);
  backdrop-filter: blur(2px);
  padding: 18px 24px;
}

.hero__trending-inner {
  display: flex;
  gap: 10px;
  max-width: 1280px;
  margin: 0 auto;
  overflow-x: auto;
}

.hero__trending-card {
  flex: 1 1 0;
  min-width: 150px;
  height: 110px;
  border: none;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  text-align: left;
  padding: 12px;
  display: flex;
  align-items: flex-start;
  transition: background 0.15s ease;
}

.hero__trending-card:hover {
  background: rgba(255, 255, 255, 0.22);
}

.hero__trending-text {
  font-size: 13px;
  line-height: 1.35;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

@media (max-width: 860px) {
  .hero {
    height: 560px;
  }
  .hero__caption {
    right: 20px;
    bottom: 230px;
  }
}

===FILE: src/components/SearchResults.tsx===
import type { SearchResult } from '../data/mockData'
import './SearchResults.css'

interface SearchResultsProps {
  keyword: string
  results: SearchResult[]
  total: number
  page: number
  totalPages: number
  onNextPage: () => void
  onPrevPage: () => void
}

export default function SearchResults({
  keyword,
  results,
  total,
  page,
  totalPages,
  onNextPage,
  onPrevPage,
}: SearchResultsProps) {
  const hasNext = page < totalPages

  return (
    <main className="results" data-testid="search-results" id="b_content">
      <div className="results__bar">
        <span className="results__count">
          约 {total.toLocaleString()} 条结果
        </span>
      </div>

      <ol className="results__list" id="b_results" data-testid="result-list">
        {results.map((item) => (
          <li key={item.id} className="b_algo results__item">
            <div className="results__url">
              <span className="results__site">{item.site}</span>
              <span className="results__path">{item.url}</span>
            </div>
            <h2 className="results__title">
              <a href="#">{highlight(item.title, keyword)}</a>
            </h2>
            <p className="results__desc">{highlight(item.description, keyword)}</p>
          </li>
        ))}
      </ol>

      <nav className="results__pagination" aria-label="分页">
        <button
          className="results__page-btn"
          onClick={onPrevPage}
          disabled={page <= 1}
          type="button"
          aria-label="上一页"
        >
          上一页
        </button>
        <span className="results__page-info">
          第 {page} / {totalPages} 页
        </span>
        <a
          className={`sb_pagN results__page-btn results__page-next${hasNext ? '' : ' results__page-btn--disabled'}`}
          title="下一页"
          aria-label="下一页"
          data-testid="next-page"
          role="button"
          tabIndex={0}
          onClick={() => hasNext && onNextPage()}
          onKeyDown={(e) => {
            if ((e.key === 'Enter' || e.key === ' ') && hasNext) {
              e.preventDefault()
              onNextPage()
            }
          }}
        >
          下一页 ›
        </a>
      </nav>
    </main>
  )
}

function highlight(text: string, keyword: string) {
  const key = keyword.trim()
  if (!key) return text
  const lower = text.toLowerCase()
  const target = key.toLowerCase()
  const parts: Array<{ text: string; mark: boolean }> = []
  let i = 0
  while (i < text.length) {
    const idx = lower.indexOf(target, i)
    if (idx === -1) {
      parts.push({ text: text.slice(i), mark: false })
      break
    }
    if (idx > i) parts.push({ text: text.slice(i, idx), mark: false })
    parts.push({ text: text.slice(idx, idx + key.length), mark: true })
    i = idx + key.length
  }
  return parts.map((p, idx) =>
    p.mark ? <strong key={idx}>{p.text}</strong> : <span key={idx}>{p.text}</span>
  )
}

===FILE: src/components/SearchResults.css===
.results {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 18px 24px 60px;
}

.results__bar {
  padding: 6px 0 12px;
  border-bottom: 1px solid #ececec;
  margin-bottom: 18px;
}

.results__count {
  font-size: 13px;
  color: rgb(118, 118, 118);
}

.results__list {
  display: flex;
  flex-direction: column;
  gap: 26px;
  max-width: 640px;
}

.results__item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.results__url {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.8px;
  color: rgb(76, 76, 76);
}

.results__site {
  color: rgb(34, 34, 34);
  font-weight: 600;
}

.results__path {
  color: rgb(118, 118, 118);
}

.results__title {
  font-size: 20px;
  font-weight: 400;
  line-height: 1.3;
}

.results__title a {
  color: #1a0dab;
}

.results__title a:hover {
  text-decoration: underline;
}

.results__title strong {
  font-weight: 600;
}

.results__desc {
  font-size: 14px;
  line-height: 1.55;
  color: rgb(43, 43, 43);
}

.results__desc strong {
  font-weight: 700;
  color: rgb(17, 17, 17);
}

.results__pagination {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 40px;
  padding-top: 22px;
  border-top: 1px solid #ececec;
  max-width: 640px;
}

.results__page-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 64px;
  height: 36px;
  padding: 0 16px;
  border: 1px solid #d2d2d2;
  border-radius: 18px;
  background: #fff;
  font-size: 14px;
  color: rgb(17, 17, 17);
  user-select: none;
}

.results__page-btn:hover {
  border-color: #0f6cbd;
  color: #0f6cbd;
}

.results__page-next {
  color: #0f6cbd;
  font-weight: 600;
}

.results__page-btn:disabled,
.results__page-btn--disabled {
  opacity: 0.45;
  cursor: not-allowed;
  pointer-events: none;
}

.results__page-info {
  font-size: 13px;
  color: rgb(76, 76, 76);
}

===FILE: src/data/mockData.ts===
export interface SearchResult {
  id: number
  title: string
  site: string
  url: string
  description: string
}

const sites = [
  { site: '百度百科', host: 'baike.baidu.com' },
  { site: '维基百科', host: 'zh.wikipedia.org' },
  { site: '知乎', host: 'www.zhihu.com' },
  { site: '微软文档', host: 'learn.microsoft.com' },
  { site: '新浪新闻', host: 'news.sina.com.cn' },
  { site: '人民网', host: 'www.people.com.cn' },
  { site: '博客园', host: 'www.cnblogs.com' },
  { site: 'CSDN', host: 'blog.csdn.net' },
  { site: 'GitHub', host: 'github.com' },
  { site: '简书', host: 'www.jianshu.com' },
]

const templates = [
  (k: string) => `${k} - 全面解读与最新资讯`,
  (k: string) => `什么是${k}？一文带你了解`,
  (k: string) => `${k}的官方介绍与使用指南`,
  (k: string) => `关于${k}，你需要知道的一切`,
  (k: string) => `${k}百科 - 定义、历史与发展`,
  (k: string) => `${k}最新动态与深度分析`,
  (k: string) => `${k}热门讨论与网友观点汇总`,
  (k: string) => `${k}相关问题与解答合集`,
  (k: string) => `${k}：从入门到精通`,
  (k: string) => `${k}的应用场景与实践案例`,
]

const descriptions = [
  (k: string) =>
    `${k}是当前广受关注的话题。本文从多个角度对${k}进行了详细介绍，涵盖背景、现状以及未来趋势，帮助你快速建立全面认识。`,
  (k: string) =>
    `想了解${k}吗？这里汇集了关于${k}的权威资料、专家解读和实用建议，内容持续更新，是获取${k}信息的可靠来源。`,
  (k: string) =>
    `本页面收录了${k}的核心知识点与常见疑问解答。无论你是初次接触还是深入研究${k}，都能在这里找到有价值的内容。`,
  (k: string) =>
    `围绕${k}的最新讨论正在进行中。我们整理了来自各方的观点与数据，为你呈现一个客观、立体的${k}全景视图。`,
  (k: string) =>
    `${k}的相关介绍、教程与案例分析尽在于此。通过通俗易懂的讲解，让你轻松掌握${k}的关键要点与实际用法。`,
]

export function search(
  keyword: string,
  page: number,
  pageSize: number
): { items: SearchResult[]; total: number } {
  // Deterministic pseudo total based on keyword length
  const total = 120 + (keyword.length % 7) * 37 + keyword.length * 11

  const start = (page - 1) * pageSize
  const items: SearchResult[] = []

  for (let i = 0; i < pageSize; i++) {
    const globalIndex = start + i
    if (globalIndex >= total) break
    const site = sites[globalIndex % sites.length]
    const titleFn = templates[globalIndex % templates.length]
    const descFn = descriptions[globalIndex % descriptions.length]
    items.push({
      id: globalIndex,
      title: titleFn(keyword),
      site: site.site,
      url: `https://${site.host}/s?q=${encodeURIComponent(keyword)}&n=${globalIndex + 1}`,
      description: descFn(keyword),
    })
  }

  return { items, total }
}