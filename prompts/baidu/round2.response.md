===FILE: package.json===
```json
{
  "name": "baidu-homepage-clone",
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
```

===FILE: vite.config.ts===
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

===FILE: tsconfig.json===
```json
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
```

===FILE: tsconfig.node.json===
```json
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
```

===FILE: index.html===
```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>百度一下，你就知道</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

===FILE: public/favicon.svg===
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <rect width="24" height="24" rx="4" fill="#4e6ef2"/>
  <text x="12" y="17" font-size="14" fill="#fff" text-anchor="middle" font-family="Arial">百</text>
</svg>
```

===FILE: src/main.tsx===
```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
)
```

===FILE: src/index.css===
```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {
  height: 100%;
}

body {
  font-family: 'PingFang SC', Arial, sans-serif;
  color: #333;
  background-color: #fff;
  -webkit-font-smoothing: antialiased;
}

#root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

a {
  color: #222;
  text-decoration: none;
}

a:hover {
  color: #4e6ef2;
}

button {
  font-family: inherit;
  cursor: pointer;
}

input,
textarea {
  font-family: inherit;
}
```

===FILE: src/App.tsx===
```tsx
import { useState } from 'react'
import Header from './components/Header'
import Logo from './components/Logo'
import SearchBox from './components/SearchBox'
import HotSearch from './components/HotSearch'
import Results from './components/Results'
import Footer from './components/Footer'
import { generateResults, PAGE_SIZE, type SearchResult } from './data/mock'
import './App.css'

export default function App() {
  const [query, setQuery] = useState('')
  const [submittedQuery, setSubmittedQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(0)

  const runSearch = (keyword: string, targetPage: number) => {
    const trimmed = keyword.trim()
    if (!trimmed) return
    const { items, total } = generateResults(trimmed, targetPage)
    setSubmittedQuery(trimmed)
    setResults(items)
    setPage(targetPage)
    setTotalPages(Math.ceil(total / PAGE_SIZE))
  }

  const handleSearch = () => {
    runSearch(query, 1)
  }

  const handlePageChange = (next: number) => {
    if (next < 1 || (totalPages && next > totalPages)) return
    runSearch(submittedQuery, next)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleHotSearch = (keyword: string) => {
    setQuery(keyword)
    runSearch(keyword, 1)
  }

  const searched = submittedQuery !== ''

  return (
    <>
      <Header />

      <main className={searched ? 'main main--searched' : 'main'}>
        <Logo compact={searched} />

        <SearchBox
          query={query}
          onQueryChange={setQuery}
          onSearch={handleSearch}
          compact={searched}
        />

        {!searched && (
          <>
            <div className="wenxin-banner">
              <span className="wenxin-icon">文心</span>
              复杂问题就找文心助手，深入思考回答更优
              <span className="wenxin-arrow">›</span>
            </div>
            <HotSearch onPick={handleHotSearch} />
          </>
        )}

        {searched && (
          <Results
            query={submittedQuery}
            results={results}
            page={page}
            totalPages={totalPages}
            onPageChange={handlePageChange}
          />
        )}
      </main>

      <Footer />
    </>
  )
}
```

===FILE: src/App.css===
```css
.main {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 20px;
}

.main--searched {
  align-items: stretch;
  padding-top: 0;
}

.wenxin-banner {
  margin-top: 28px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  background: #f6f7fe;
  border-radius: 999px;
  font-size: 14px;
  color: #626675;
  cursor: pointer;
}

.wenxin-banner:hover {
  background: #eef0fd;
}

.wenxin-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 7px;
  border-radius: 6px;
  background: linear-gradient(135deg, #4e6ef2, #6d8bff);
  color: #fff;
  font-size: 12px;
}

.wenxin-arrow {
  color: #9195a3;
  font-size: 16px;
}
```

===FILE: src/components/Header.tsx===
```tsx
import './Header.css'

const NAV_ITEMS = [
  '新闻',
  'hao123',
  '地图',
  '贴吧',
  '视频',
  '图片',
  '网盘',
  '文库',
  '文心',
  '搭子DuMate',
  '更多',
]

export default function Header() {
  return (
    <header className="site-header">
      <nav className="site-nav">
        {NAV_ITEMS.map((item) => (
          <a key={item} className="nav-link" href="#">
            {item}
          </a>
        ))}
      </nav>
      <div className="header-right">
        <a className="nav-link" href="#">
          设置
        </a>
        <button className="login-btn" type="button">
          登录
        </button>
      </div>
    </header>
  )
}
```

===FILE: src/components/Header.css===
```css
.site-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 22px;
  height: 56px;
}

.site-nav {
  display: flex;
  align-items: center;
  gap: 22px;
  flex-wrap: wrap;
}

.nav-link {
  font-size: 14px;
  color: #222;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.login-btn {
  border: none;
  background: #4e6ef2;
  color: #fff;
  font-size: 13px;
  padding: 6px 16px;
  border-radius: 6px;
}

.login-btn:hover {
  background: #4264e0;
}
```

===FILE: src/components/Logo.tsx===
```tsx
import './Logo.css'

interface LogoProps {
  compact?: boolean
}

export default function Logo({ compact = false }: LogoProps) {
  return (
    <div className={compact ? 'logo logo--compact' : 'logo'}>
      <span className="logo-b">B</span>
      <span className="logo-a">a</span>
      <span className="logo-i">i</span>
      <span className="logo-d">d</span>
      <span className="logo-u">u</span>
      <span className="logo-cn">百度</span>
    </div>
  )
}
```

===FILE: src/components/Logo.css===
```css
.logo {
  margin-top: 60px;
  margin-bottom: 22px;
  font-family: Arial, sans-serif;
  font-weight: 700;
  font-size: 52px;
  letter-spacing: -1px;
  user-select: none;
}

.logo--compact {
  margin-top: 18px;
  margin-bottom: 14px;
  font-size: 30px;
}

.logo-b {
  color: #2932e1;
}
.logo-a {
  color: #4e6ef2;
}
.logo-i {
  color: #4e6ef2;
}
.logo-d {
  color: #2932e1;
}
.logo-u {
  color: #4e6ef2;
}
.logo-cn {
  color: #2932e1;
  margin-left: 4px;
}
```

===FILE: src/components/SearchBox.tsx===
```tsx
import { type KeyboardEvent } from 'react'
import './SearchBox.css'

interface SearchBoxProps {
  query: string
  onQueryChange: (value: string) => void
  onSearch: () => void
  compact?: boolean
}

export default function SearchBox({
  query,
  onQueryChange,
  onSearch,
  compact = false,
}: SearchBoxProps) {
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      onSearch()
    }
  }

  return (
    <div className={compact ? 'search-box search-box--compact' : 'search-box'}>
      <div className="search-field">
        <textarea
          data-testid="search-input"
          className="search-input"
          value={query}
          placeholder="演员刘洵去世"
          rows={1}
          onChange={(e) => onQueryChange(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <div className="search-actions">
          <span className="action-icon" title="语音搜索" aria-label="语音搜索">
            🎤
          </span>
          <span className="action-icon" title="上传" aria-label="上传">
            📎
          </span>
          <span className="action-icon" title="图片搜索" aria-label="图片搜索">
            🖼️
          </span>
          <button
            data-testid="search-button"
            className="search-button"
            type="button"
            onClick={onSearch}
          >
            百度一下
          </button>
        </div>
      </div>
    </div>
  )
}
```

===FILE: src/components/SearchBox.css===
```css
.search-box {
  width: 100%;
  max-width: 800px;
  margin-top: 8px;
}

.search-box--compact {
  max-width: 640px;
  margin-left: 0;
}

.search-field {
  position: relative;
  border: 2px solid #4e6ef2;
  border-radius: 14px;
  padding: 14px 18px 50px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s ease;
}

.search-box--compact .search-field {
  padding: 10px 14px 10px;
  display: flex;
  align-items: center;
}

.search-field:focus-within {
  box-shadow: 0 4px 18px rgba(78, 110, 242, 0.18);
}

.search-input {
  width: 100%;
  border: none;
  outline: none;
  resize: none;
  font-size: 16px;
  line-height: 24px;
  color: #222;
  background: transparent;
  overflow: hidden;
}

.search-box--compact .search-input {
  font-size: 15px;
}

.search-input::placeholder {
  color: #9195a3;
}

.search-actions {
  position: absolute;
  right: 14px;
  bottom: 10px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.search-box--compact .search-actions {
  position: static;
  margin-left: 12px;
}

.action-icon {
  font-size: 16px;
  color: #9195a3;
  cursor: pointer;
  opacity: 0.75;
}

.search-box--compact .action-icon {
  display: none;
}

.action-icon:hover {
  opacity: 1;
}

.search-button {
  border: none;
  background: linear-gradient(135deg, #4e6ef2, #4662e8);
  color: #fff;
  font-size: 16px;
  padding: 8px 22px;
  border-radius: 10px;
  white-space: nowrap;
}

.search-box--compact .search-button {
  font-size: 14px;
  padding: 7px 18px;
}

.search-button:hover {
  background: linear-gradient(135deg, #4264e0, #3a5ad8);
}
```

===FILE: src/components/HotSearch.tsx===
```tsx
import './HotSearch.css'

interface HotSearchProps {
  onPick: (keyword: string) => void
}

interface HotItem {
  rank: number
  title: string
  tag?: 'top' | 'new' | 'hot'
}

const LEFT: HotItem[] = [
  { rank: 0, title: '加快高水平科技自立自强', tag: 'top' },
  { rank: 1, title: '湖北一社区书记多看一眼救下128人', tag: 'new' },
  { rank: 2, title: '印政府警告宝莱坞：不得抨击中国', tag: 'hot' },
  { rank: 3, title: '国家首次专门发文 这四类人群受益' },
  { rank: 4, title: '车手张秀军意外离世 留下3个孩子', tag: 'new' },
]

const RIGHT: HotItem[] = [
  { rank: 5, title: '中国公民在菲监狱离世 中方严正交涉' },
  { rank: 6, title: '老人与邻居互殴次日自缢 法院判了' },
  { rank: 7, title: '演员刘洵去世 曾参演《九品芝麻官》', tag: 'new' },
  { rank: 8, title: '17岁女生打赏650万 起诉退款被驳回' },
  { rank: 9, title: '市民打12345求干预天气 当地回应', tag: 'hot' },
]

function rankColor(rank: number) {
  if (rank === 0) return '#fe2d46'
  if (rank === 1) return '#f60'
  if (rank === 2) return '#ff9f1f'
  return '#9195a3'
}

function Tag({ tag }: { tag?: HotItem['tag'] }) {
  if (!tag) return null
  const map = { top: '顶', new: '新', hot: '热' }
  const colors = { top: '#fe2d46', new: '#fe2d46', hot: '#f60' }
  return (
    <span className="hot-tag" style={{ background: colors[tag] }}>
      {map[tag]}
    </span>
  )
}

export default function HotSearch({ onPick }: HotSearchProps) {
  const renderItem = (item: HotItem) => (
    <li key={item.rank} className="hot-item" onClick={() => onPick(item.title)}>
      {item.rank === 0 ? (
        <span className="hot-rank hot-rank--top" style={{ color: rankColor(item.rank) }}>
          ↑
        </span>
      ) : (
        <span className="hot-rank" style={{ color: rankColor(item.rank) }}>
          {item.rank}
        </span>
      )}
      <span className="hot-title">{item.title}</span>
      <Tag tag={item.tag} />
    </li>
  )

  return (
    <section className="hot-search">
      <div className="hot-head">
        <span className="hot-head-title">
          百度<span className="hot-head-accent">热</span>搜
          <span className="hot-head-arrow">›</span>
        </span>
        <span className="hot-refresh">⟳ 换一换</span>
      </div>
      <div className="hot-columns">
        <ul className="hot-col">{LEFT.map(renderItem)}</ul>
        <ul className="hot-col">{RIGHT.map(renderItem)}</ul>
      </div>
    </section>
  )
}
```

===FILE: src/components/HotSearch.css===
```css
.hot-search {
  width: 100%;
  max-width: 800px;
  margin-top: 36px;
}

.hot-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.hot-head-title {
  font-size: 18px;
  font-weight: 700;
  color: #222;
}

.hot-head-accent {
  color: #fe2d46;
}

.hot-head-arrow {
  color: #9195a3;
  margin-left: 4px;
  font-weight: 400;
}

.hot-refresh {
  font-size: 13px;
  color: #9195a3;
  cursor: pointer;
}

.hot-refresh:hover {
  color: #4e6ef2;
}

.hot-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 48px;
}

.hot-col {
  list-style: none;
}

.hot-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 4px;
  cursor: pointer;
  border-radius: 6px;
}

.hot-item:hover {
  background: #f6f7fe;
}

.hot-item:hover .hot-title {
  color: #4e6ef2;
}

.hot-rank {
  width: 16px;
  text-align: center;
  font-size: 14px;
  font-weight: 700;
  font-style: italic;
}

.hot-rank--top {
  font-style: normal;
}

.hot-title {
  flex: 1;
  font-size: 14px;
  color: #222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hot-tag {
  color: #fff;
  font-size: 11px;
  padding: 1px 5px;
  border-radius: 4px;
}
```

===FILE: src/components/Results.tsx===
```tsx
import './Results.css'
import { type SearchResult } from '../data/mock'

interface ResultsProps {
  query: string
  results: SearchResult[]
  page: number
  totalPages: number
  onPageChange: (page: number) => void
}

export default function Results({
  query,
  results,
  page,
  totalPages,
  onPageChange,
}: ResultsProps) {
  const pageNumbers = buildPageNumbers(page, totalPages)

  return (
    <section className="results-wrap">
      <p className="results-count">
        找到约 {(results.length * totalPages * 137 + 5021).toLocaleString()} 个结果
      </p>

      <ul data-testid="result-list" className="result-list">
        {results.map((item) => (
          <li key={item.id} className="result-item">
            <a className="result-title" href="#">
              {item.title}
            </a>
            <div className="result-meta">
              <span className="result-source">{item.source}</span>
              <span className="result-date">{item.date}</span>
            </div>
            <p className="result-summary">{item.summary}</p>
            <a className="result-url" href="#">
              {item.url}
            </a>
          </li>
        ))}
      </ul>

      <nav className="pagination" data-testid="pagination">
        <button
          className="page-btn page-prev"
          type="button"
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
          data-testid="prev-page"
        >
          上一页
        </button>

        {pageNumbers.map((n) => (
          <button
            key={n}
            className={n === page ? 'page-btn page-num page-num--active' : 'page-btn page-num'}
            type="button"
            onClick={() => onPageChange(n)}
          >
            {n}
          </button>
        ))}

        <button
          className="page-btn page-next"
          type="button"
          disabled={page >= totalPages}
          onClick={() => onPageChange(page + 1)}
          data-testid="next-page"
        >
          下一页 ›
        </button>
      </nav>
    </section>
  )
}

function buildPageNumbers(current: number, total: number): number[] {
  const span = 5
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + span - 1)
  start = Math.max(1, end - span + 1)
  const pages: number[] = []
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
}
```

===FILE: src/components/Results.css===
```css
.results-wrap {
  width: 100%;
  max-width: 760px;
  margin: 18px auto 0;
  padding: 0 8px 40px;
}

.results-count {
  font-size: 13px;
  color: #9195a3;
  margin-bottom: 16px;
}

.result-list {
  list-style: none;
}

.result-item {
  margin-bottom: 26px;
}

.result-title {
  display: inline-block;
  font-size: 18px;
  line-height: 1.4;
  color: #2440b3;
  font-weight: 500;
  margin-bottom: 4px;
}

.result-title:hover {
  text-decoration: underline;
  color: #2440b3;
}

.result-meta {
  display: flex;
  gap: 10px;
  font-size: 13px;
  color: #9195a3;
  margin-bottom: 4px;
}

.result-source {
  color: #626675;
}

.result-summary {
  font-size: 14px;
  line-height: 1.7;
  color: #333;
  margin-bottom: 5px;
}

.result-url {
  font-size: 13px;
  color: #008000;
}

.result-url:hover {
  color: #008000;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 30px;
  flex-wrap: wrap;
}

.page-btn {
  border: 1px solid #e3e5ec;
  background: #fff;
  color: #4e6ef2;
  font-size: 14px;
  padding: 7px 13px;
  border-radius: 8px;
  min-width: 38px;
}

.page-btn:hover:not(:disabled) {
  border-color: #4e6ef2;
  background: #f6f7fe;
}

.page-num--active {
  background: #4e6ef2;
  color: #fff;
  border-color: #4e6ef2;
}

.page-num--active:hover {
  background: #4e6ef2 !important;
  color: #fff;
}

.page-btn:disabled {
  color: #bbb;
  cursor: not-allowed;
  background: #fafafa;
}
```

===FILE: src/components/Footer.tsx===
```tsx
import './Footer.css'

const LINKS = [
  '关于百度',
  'About Baidu',
  '使用百度前必读',
  '帮助中心',
  '企业推广',
  '京公网安备11000002000001号',
  '京ICP证030173号',
  '互联网新闻信息服务许可11220180008',
  '网络文化经营许可证：京网文〔2026〕0171-042号',
]

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-links">
        {LINKS.map((link) => (
          <a key={link} className="footer-link" href="#">
            {link}
          </a>
        ))}
      </div>
    </footer>
  )
}
```

===FILE: src/components/Footer.css===
```css
.site-footer {
  width: 100%;
  padding: 16px 20px;
  background: #fbfbfb;
  border-top: 1px solid #f0f0f0;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px 18px;
}

.footer-link {
  font-size: 12px;
  color: #9195a3;
}

.footer-link:hover {
  color: #4e6ef2;
}
```

===FILE: src/data/mock.ts===
```ts
export interface SearchResult {
  id: string
  title: string
  source: string
  date: string
  summary: string
  url: string
}

export const PAGE_SIZE = 10

const SOURCES = [
  '百度百科',
  '知乎',
  '新浪新闻',
  '人民网',
  '百家号',
  '腾讯网',
  '搜狐网',
  '今日头条',
  '中国新闻网',
  '澎湃新闻',
]

const SUMMARY_TEMPLATES = [
  (k: string) => `${k}是近期备受关注的话题，相关讨论持续升温。本文从多个角度详细介绍${k}的背景、最新进展以及社会各界的看法，帮助你快速全面了解。`,
  (k: string) => `关于${k}的最新报道。据多方消息，${k}的相关情况正在进一步明确，本文整理了权威来源的信息，并对后续发展进行了分析。`,
  (k: string) => `${k}_百度百科。${k}指的是一个被广泛讨论的事物或事件，词条收录了它的定义、由来、特点与相关延伸内容，资料持续更新中。`,
  (k: string) => `有网友提问：如何看待${k}？高赞回答从专业视角出发，结合实际案例，对${k}进行了深入浅出的剖析，获得众多用户认可。`,
  (k: string) => `${k}最新视频合集。汇集与${k}相关的高清视频内容，包含现场记录、专家解读和网友评论，时长更新，欢迎观看。`,
  (k: string) => `深度解读${k}：你需要知道的几件事。本文围绕${k}梳理了关键时间线与核心要点，并附上常见问题解答，内容详实可靠。`,
]

function dateForIndex(globalIndex: number): string {
  const base = new Date('2026-01-15T00:00:00')
  base.setDate(base.getDate() - globalIndex)
  const y = base.getFullYear()
  const m = String(base.getMonth() + 1).padStart(2, '0')
  const d = String(base.getDate()).padStart(2, '0')
  return `${y}年${m}月${d}日`
}

export function generateResults(
  keyword: string,
  page: number
): { items: SearchResult[]; total: number } {
  const total = 73
  const startIndex = (page - 1) * PAGE_SIZE
  const items: SearchResult[] = []

  for (let i = 0; i < PAGE_SIZE; i++) {
    const globalIndex = startIndex + i
    if (globalIndex >= total) break

    const source = SOURCES[globalIndex % SOURCES.length]
    const summaryFn = SUMMARY_TEMPLATES[globalIndex % SUMMARY_TEMPLATES.length]
    const titleSuffix =
      globalIndex % SUMMARY_TEMPLATES.length === 2
        ? `${keyword}_百度百科`
        : `${keyword} - ${source}相关内容 ${globalIndex + 1}`

    items.push({
      id: `${keyword}-${globalIndex}`,
      title: titleSuffix,
      source,
      date: dateForIndex(globalIndex),
      summary: summaryFn(keyword),
      url: `https://www.example.com/s?wd=${encodeURIComponent(keyword)}&pn=${globalIndex}`,
    })
  }

  return { items, total }
}
```