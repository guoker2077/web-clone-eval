===FILE: package.json===
```json
{
  "name": "baidu-clone",
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>百度一下，你就知道</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
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
  </StrictMode>,
)
```

===FILE: src/index.css===
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  height: 100%;
}

body {
  font-family: 'PingFang SC', Arial, sans-serif;
  color: #222;
  background: #fff;
  -webkit-font-smoothing: antialiased;
}

a {
  text-decoration: none;
  color: #2440b3;
}

a:hover {
  text-decoration: underline;
}

input,
button,
textarea {
  font-family: inherit;
}
```

===FILE: src/data/mockResults.ts===
```ts
export interface SearchResult {
  title: string
  url: string
  source: string
  date: string
  abstract: string
}

const templates: Array<(kw: string, i: number) => SearchResult> = [
  (kw, i) => ({
    title: `${kw}_百度百科`,
    url: 'https://baike.baidu.com',
    source: '百度百科',
    date: '2024-3-12',
    abstract: `${kw}是近期备受关注的话题。本词条详细介绍了${kw}的基本含义、发展历程、相关背景以及社会各界的评价，帮助你快速全面地了解${kw}的方方面面。`,
  }),
  (kw, i) => ({
    title: `关于${kw}的最新消息汇总 - 新闻中心`,
    url: 'https://news.baidu.com',
    source: '百度新闻',
    date: '1小时前',
    abstract: `综合多家媒体报道，${kw}相关进展持续更新。记者从权威渠道获悉，事件后续将受到广泛关注，更多细节正在进一步核实中，请以官方发布为准。`,
  }),
  (kw, i) => ({
    title: `${kw}怎么样？网友真实评价与体验分享`,
    url: 'https://zhidao.baidu.com',
    source: '百度知道',
    date: '2024-2-28',
    abstract: `针对“${kw}”这个问题，已有多位网友给出了详细解答。综合大家的回答来看，关于${kw}的看法各有不同，建议结合自身实际情况理性参考。`,
  }),
  (kw, i) => ({
    title: `${kw}全面解析：你想知道的都在这里`,
    url: 'https://wenku.baidu.com',
    source: '百度文库',
    date: '2024-1-15',
    abstract: `本文档对${kw}进行了系统梳理，涵盖核心要点、常见问题与实用建议。内容深入浅出，适合不同需求的读者阅读和收藏。`,
  }),
  (kw, i) => ({
    title: `${kw} - 官方网站`,
    url: 'https://www.example.com',
    source: '官方',
    date: '2024-3-1',
    abstract: `${kw}官方门户，提供最权威、最及时的资讯与服务。访问官网获取一手信息，避免被不实内容误导。`,
  }),
]

export function generateResults(keyword: string, page: number, pageSize = 8): SearchResult[] {
  const kw = keyword.trim() || '百度'
  const results: SearchResult[] = []
  for (let i = 0; i < pageSize; i++) {
    const globalIndex = (page - 1) * pageSize + i
    const tpl = templates[globalIndex % templates.length]
    const r = tpl(kw, globalIndex)
    results.push({
      ...r,
      title: globalIndex < templates.length ? r.title : `${r.title}（第${globalIndex + 1}条）`,
    })
  }
  return results
}

export const TOTAL_PAGES = 10
```

===FILE: src/components/Header.tsx===
```tsx
import './Header.css'

const navItems = [
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
]

export default function Header() {
  return (
    <header className="top-nav">
      <ul className="nav-list">
        {navItems.map((item) => (
          <li key={item}>
            <a href="#" onClick={(e) => e.preventDefault()}>
              {item}
            </a>
          </li>
        ))}
        <li className="more">
          <a href="#" onClick={(e) => e.preventDefault()}>
            更多
          </a>
        </li>
      </ul>
    </header>
  )
}
```

===FILE: src/components/Header.css===
```css
.top-nav {
  width: 100%;
  padding: 16px 24px;
}

.nav-list {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 26px;
  font-size: 13px;
}

.nav-list a {
  color: #222;
  font-size: 13px;
}

.nav-list a:hover {
  color: #315efb;
  text-decoration: none;
}

.nav-list .more a {
  color: #222;
}
```

===FILE: src/components/Logo.tsx===
```tsx
import './Logo.css'

export default function Logo() {
  return (
    <div className="logo" aria-label="百度">
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
  display: flex;
  align-items: flex-end;
  justify-content: center;
  font-family: Arial, sans-serif;
  font-weight: 700;
  font-size: 50px;
  line-height: 1;
  user-select: none;
}

.logo span {
  letter-spacing: -1px;
}

.logo-b {
  color: #4e6ef2;
}
.logo-a {
  color: #4e6ef2;
}
.logo-i {
  color: #f5a623;
}
.logo-d {
  color: #4e6ef2;
}
.logo-u {
  color: #4caf50;
}
.logo-cn {
  color: #4e6ef2;
  margin-left: 4px;
  font-size: 50px;
}
```

===FILE: src/components/SearchBox.tsx===
```tsx
import { useState } from 'react'
import './SearchBox.css'

interface SearchBoxProps {
  initialValue?: string
  compact?: boolean
  onSearch: (keyword: string) => void
}

export default function SearchBox({ initialValue = '', compact = false, onSearch }: SearchBoxProps) {
  const [value, setValue] = useState(initialValue)

  const submit = () => {
    if (value.trim().length === 0) return
    onSearch(value.trim())
  }

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className={compact ? 'search-box compact' : 'search-box'}>
      <div className="search-field">
        <textarea
          data-testid="search-input"
          className="search-input"
          name="wd"
          rows={1}
          placeholder="演员刘洵去世"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKeyDown}
        />
        <div className="search-tools">
          <span className="tool-icon" title="语音">
            🎤
          </span>
          <span className="tool-icon" title="附件">
            📎
          </span>
          <span className="tool-icon" title="拍照">
            📷
          </span>
        </div>
      </div>
      <button
        data-testid="search-button"
        type="submit"
        className="search-btn"
        onClick={submit}
      >
        百度一下
      </button>
    </div>
  )
}
```

===FILE: src/components/SearchBox.css===
```css
.search-box {
  display: flex;
  align-items: flex-start;
  width: 800px;
  max-width: 90vw;
  margin: 0 auto;
  gap: 0;
}

.search-field {
  position: relative;
  flex: 1;
  border: 2px solid #c4c7ce;
  border-radius: 12px;
  background: #fff;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  display: flex;
  flex-direction: column;
  min-height: 100px;
}

.search-field:focus-within {
  border-color: #4e6ef2;
  box-shadow: 0 2px 12px rgba(78, 110, 242, 0.12);
}

.search-input {
  width: 100%;
  border: none;
  outline: none;
  resize: none;
  padding: 16px 18px 0;
  font-size: 16px;
  line-height: 24px;
  color: #222;
  background: transparent;
  flex: 1;
}

.search-input::placeholder {
  color: #9195a3;
}

.search-tools {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 14px;
  padding: 0 18px 12px;
}

.tool-icon {
  cursor: pointer;
  font-size: 16px;
  opacity: 0.7;
  filter: grayscale(0.4);
}

.tool-icon:hover {
  opacity: 1;
}

.search-btn {
  align-self: flex-end;
  margin-left: 18px;
  margin-bottom: 12px;
  height: 44px;
  padding: 0 28px;
  background: #4e6ef2;
  color: #fff;
  font-size: 16px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease;
}

.search-btn:hover {
  background: #4662d9;
}

/* compact mode for results page */
.search-box.compact {
  width: 640px;
  margin: 0;
}

.search-box.compact .search-field {
  min-height: auto;
  border-radius: 10px;
  border-width: 1px;
  flex-direction: row;
  align-items: center;
}

.search-box.compact .search-input {
  padding: 10px 14px;
  font-size: 15px;
  line-height: 22px;
  height: 40px;
  overflow: hidden;
}

.search-box.compact .search-tools {
  padding: 0 12px 0 0;
}

.search-box.compact .search-btn {
  align-self: center;
  margin-bottom: 0;
  height: 42px;
  border-radius: 0 10px 10px 0;
  margin-left: 0;
}
```

===FILE: src/components/HotSearch.tsx===
```tsx
import './HotSearch.css'

interface HotItem {
  rank: number
  text: string
  tag?: 'top' | 'new' | 'hot'
}

const hotItems: HotItem[] = [
  { rank: 0, text: '加快高水平科技自立自强', tag: 'top' },
  { rank: 5, text: '中国公民在菲监狱离世 中方严正交涉' },
  { rank: 1, text: '湖北一社区书记多看一眼救下128人', tag: 'new' },
  { rank: 6, text: '老人与邻居互殴次日自缢 法院判了' },
  { rank: 2, text: '印政府警告宝莱坞：不得�200击中国', tag: 'hot' },
  { rank: 7, text: '演员刘洵去世 曾参演《九品芝麻官》', tag: 'new' },
  { rank: 3, text: '国家首次专门发文 这四类人群受益' },
  { rank: 8, text: '17岁女生打赏650万 起诉退款被驳回' },
  { rank: 4, text: '车手张秀军意外离世 留下3个孩子', tag: 'new' },
  { rank: 9, text: '市民打12345求干预天气 当地回应', tag: 'hot' },
]

const tagLabel: Record<string, string> = {
  new: '新',
  hot: '热',
}

interface HotSearchProps {
  onSelect: (text: string) => void
}

export default function HotSearch({ onSelect }: HotSearchProps) {
  return (
    <div className="hot-search">
      <div className="hot-header">
        <span className="hot-title">
          百度<span className="hot-title-accent">热搜</span> ›
        </span>
        <span className="hot-change">↻ 换一换</span>
      </div>
      <ul className="hot-list">
        {hotItems.map((item, idx) => (
          <li key={idx} className="hot-item" onClick={() => onSelect(item.text)}>
            <span className={`hot-rank rank-${item.rank}`}>{item.rank}</span>
            <span className="hot-text">{item.text}</span>
            {item.tag && item.tag !== 'top' && (
              <span className={`hot-tag tag-${item.tag}`}>{tagLabel[item.tag]}</span>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

===FILE: src/components/HotSearch.css===
```css
.hot-search {
  width: 800px;
  max-width: 90vw;
  margin: 30px auto 0;
}

.hot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 6px 10px;
}

.hot-title {
  font-size: 18px;
  font-weight: 700;
  color: #222;
}

.hot-title-accent {
  color: #4e6ef2;
}

.hot-change {
  font-size: 13px;
  color: #9195a3;
  cursor: pointer;
}

.hot-change:hover {
  color: #4e6ef2;
}

.hot-list {
  list-style: none;
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 40px;
  row-gap: 4px;
}

.hot-item {
  display: flex;
  align-items: center;
  padding: 7px 6px;
  border-radius: 6px;
  cursor: pointer;
  gap: 8px;
}

.hot-item:hover {
  background: #f6f7fe;
}

.hot-rank {
  width: 18px;
  text-align: center;
  font-size: 14px;
  color: #9195a3;
  font-style: italic;
  flex-shrink: 0;
}

.hot-rank.rank-0 {
  color: #fe2d46;
}
.hot-rank.rank-1 {
  color: #f60;
}
.hot-rank.rank-2 {
  color: #faa90e;
}

.hot-text {
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hot-item:hover .hot-text {
  color: #315efb;
}

.hot-tag {
  font-size: 11px;
  color: #fff;
  border-radius: 3px;
  padding: 0 4px;
  line-height: 16px;
  flex-shrink: 0;
}

.tag-new {
  background: #fe2d46;
}

.tag-hot {
  background: #ff6600;
}
```

===FILE: src/components/ResultList.tsx===
```tsx
import type { SearchResult } from '../data/mockResults'
import './ResultList.css'

interface ResultListProps {
  keyword: string
  results: SearchResult[]
  page: number
  totalPages: number
  onPageChange: (page: number) => void
}

export default function ResultList({
  keyword,
  results,
  page,
  totalPages,
  onPageChange,
}: ResultListProps) {
  const pageNumbers: number[] = []
  const start = Math.max(1, page - 4)
  const end = Math.min(totalPages, start + 9)
  for (let p = start; p <= end; p++) pageNumbers.push(p)

  return (
    <div className="result-section">
      <div className="result-meta">
        百度为您找到相关结果约 {(1230000).toLocaleString()} 个
      </div>
      <ul className="result-list" data-testid="result-list">
        {results.map((r, i) => (
          <li className="result-item" key={`${page}-${i}`}>
            <h3 className="result-title">
              <a href={r.url} onClick={(e) => e.preventDefault()}>
                {r.title}
              </a>
            </h3>
            <p className="result-abstract">{r.abstract}</p>
            <div className="result-foot">
              <span className="result-source">{r.source}</span>
              <span className="result-date">{r.date}</span>
            </div>
          </li>
        ))}
      </ul>

      <div className="pagination" data-testid="pagination">
        {page > 1 && (
          <button
            className="page-btn"
            data-testid="prev-page"
            onClick={() => onPageChange(page - 1)}
          >
            上一页
          </button>
        )}
        {pageNumbers.map((p) => (
          <button
            key={p}
            className={p === page ? 'page-num active' : 'page-num'}
            onClick={() => onPageChange(p)}
          >
            {p}
          </button>
        ))}
        {page < totalPages && (
          <button
            className="page-btn"
            data-testid="next-page"
            onClick={() => onPageChange(page + 1)}
          >
            下一页 ›
          </button>
        )}
      </div>
    </div>
  )
}
```

===FILE: src/components/ResultList.css===
```css
.result-section {
  width: 640px;
  max-width: 90vw;
  margin: 20px 0 60px;
  padding-left: 24px;
}

.result-meta {
  font-size: 13px;
  color: #9195a3;
  margin-bottom: 16px;
}

.result-list {
  list-style: none;
}

.result-item {
  margin-bottom: 24px;
}

.result-title {
  font-size: 18px;
  font-weight: 400;
  line-height: 1.4;
  margin-bottom: 6px;
}

.result-title a {
  color: #2440b3;
}

.result-title a:visited {
  color: #771caa;
}

.result-abstract {
  font-size: 14px;
  line-height: 1.7;
  color: #333;
  margin-bottom: 6px;
}

.result-foot {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: #9195a3;
}

.result-source {
  color: #626675;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 30px;
  flex-wrap: wrap;
}

.page-num,
.page-btn {
  min-width: 34px;
  height: 34px;
  padding: 0 10px;
  border: 1px solid #e0e0e0;
  background: #fff;
  color: #2440b3;
  font-size: 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.page-num:hover,
.page-btn:hover {
  border-color: #4e6ef2;
  background: #f6f7fe;
}

.page-num.active {
  background: #4e6ef2;
  border-color: #4e6ef2;
  color: #fff;
  font-weight: 700;
  cursor: default;
}
```

===FILE: src/components/Footer.tsx===
```tsx
import './Footer.css'

const links = [
  '关于百度',
  'About Baidu',
  '使用百度前必读',
  '帮助中心',
  '企业推广',
]

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-links">
        {links.map((l) => (
          <a key={l} href="#" onClick={(e) => e.preventDefault()}>
            {l}
          </a>
        ))}
      </div>
      <div className="footer-info">
        京公网安备11000002000001号 京ICP证030173号 互联网新闻信息服务许可11220180008
        网络文化经营许可证：京网文〔2026〕0171-042号
      </div>
    </footer>
  )
}
```

===FILE: src/components/Footer.css===
```css
.footer {
  width: 100%;
  padding: 18px 24px;
  text-align: center;
  font-size: 12px;
  color: #9195a3;
  border-top: 1px solid #f1f1f1;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 18px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.footer-links a {
  color: #9195a3;
  font-size: 12px;
}

.footer-links a:hover {
  color: #4e6ef2;
}

.footer-info {
  line-height: 1.6;
}
```

===FILE: src/App.tsx===
```tsx
import { useState } from 'react'
import Header from './components/Header'
import Logo from './components/Logo'
import SearchBox from './components/SearchBox'
import HotSearch from './components/HotSearch'
import ResultList from './components/ResultList'
import Footer from './components/Footer'
import { generateResults, TOTAL_PAGES, type SearchResult } from './data/mockResults'
import './App.css'

export default function App() {
  const [submitted, setSubmitted] = useState(false)
  const [keyword, setKeyword] = useState('')
  const [page, setPage] = useState(1)
  const [results, setResults] = useState<SearchResult[]>([])

  const runSearch = (kw: string, targetPage: number) => {
    setKeyword(kw)
    setPage(targetPage)
    setResults(generateResults(kw, targetPage))
    setSubmitted(true)
  }

  const handleSearch = (kw: string) => {
    runSearch(kw, 1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handlePageChange = (p: number) => {
    runSearch(keyword, p)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  if (!submitted) {
    return (
      <div className="app home">
        <Header />
        <main className="home-main">
          <div className="logo-wrap">
            <Logo />
          </div>
          <SearchBox onSearch={handleSearch} />
          <div className="ai-tip">
            <span className="ai-tip-icon">文心</span>
            复杂问题就找文心助手，深入思考回答更优 ›
          </div>
          <HotSearch onSelect={handleSearch} />
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="app results">
      <div className="results-header">
        <div className="results-header-inner">
          <div className="results-logo" onClick={() => setSubmitted(false)}>
            <Logo />
          </div>
          <SearchBox initialValue={keyword} compact onSearch={handleSearch} />
        </div>
      </div>
      <main className="results-main">
        <ResultList
          keyword={keyword}
          results={results}
          page={page}
          totalPages={TOTAL_PAGES}
          onPageChange={handlePageChange}
        />
      </main>
      <Footer />
    </div>
  )
}
```

===FILE: src/App.css===
```css
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ---------- Home ---------- */
.home-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
}

.logo-wrap {
  margin-bottom: 28px;
}

.ai-tip {
  margin-top: 22px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #626675;
  background: #f6f7fe;
  border-radius: 18px;
  padding: 8px 18px;
  cursor: pointer;
}

.ai-tip:hover {
  background: #eef0fd;
}

.ai-tip-icon {
  background: linear-gradient(135deg, #4e6ef2, #6a85ff);
  color: #fff;
  font-size: 12px;
  border-radius: 10px;
  padding: 2px 8px;
}

/* ---------- Results ---------- */
.results-header {
  border-bottom: 1px solid #f1f1f1;
  padding: 14px 0;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
}

.results-header-inner {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 0 40px;
  max-width: 1100px;
}

.results-logo {
  cursor: pointer;
  transform: scale(0.6);
  transform-origin: left center;
  flex-shrink: 0;
}

.results-main {
  flex: 1;
  padding: 0 40px;
}
```