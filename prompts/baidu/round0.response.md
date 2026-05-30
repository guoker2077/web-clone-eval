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
    "typescript": "^5.5.4",
    "vite": "^5.4.2"
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#4e6ef2"/>
  <text x="16" y="23" font-size="20" font-family="Arial" font-weight="bold" fill="#fff" text-anchor="middle">百</text>
</svg>
```

===FILE: src/main.tsx===
```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles/global.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
)
```

===FILE: src/App.tsx===
```tsx
import { useState } from 'react'
import TopNav from './components/TopNav'
import Logo from './components/Logo'
import SearchBox from './components/SearchBox'
import HotSearch from './components/HotSearch'
import SearchResults from './components/SearchResults'
import Footer from './components/Footer'
import { searchMock } from './data/mock'
import type { SearchResult } from './data/mock'
import './styles/app.css'

const PAGE_SIZE = 5

export default function App() {
  const [query, setQuery] = useState('')
  const [submittedQuery, setSubmittedQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [page, setPage] = useState(1)
  const [searched, setSearched] = useState(false)

  const runSearch = (keyword: string) => {
    const trimmed = keyword.trim()
    if (!trimmed) return
    setSubmittedQuery(trimmed)
    setResults(searchMock(trimmed))
    setPage(1)
    setSearched(true)
  }

  const handleSubmit = () => runSearch(query)

  const handleHotClick = (text: string) => {
    setQuery(text)
    runSearch(text)
  }

  const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE))
  const pageResults = results.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  const handleNextPage = () => {
    setPage((p) => Math.min(totalPages, p + 1))
  }

  const handlePrevPage = () => {
    setPage((p) => Math.max(1, p - 1))
  }

  return (
    <div className="page">
      <TopNav />
      <main className={`main ${searched ? 'main--searched' : ''}`}>
        <Logo />
        <SearchBox
          value={query}
          onChange={setQuery}
          onSubmit={handleSubmit}
        />

        {!searched && (
          <>
            <div className="wenxin-banner">
              <span className="wenxin-icon">文心</span>
              复杂问题就找文心助手，深入思考回答更优
              <span className="wenxin-arrow">›</span>
            </div>
            <HotSearch onItemClick={handleHotClick} />
          </>
        )}

        {searched && (
          <SearchResults
            keyword={submittedQuery}
            results={pageResults}
            totalCount={results.length}
            page={page}
            totalPages={totalPages}
            onNextPage={handleNextPage}
            onPrevPage={handlePrevPage}
          />
        )}
      </main>
      <Footer />
    </div>
  )
}
```

===FILE: src/components/TopNav.tsx===
```tsx
import './TopNav.css'

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
  '更多',
]

export default function TopNav() {
  return (
    <nav className="top-nav">
      <div className="top-nav__links">
        {navItems.map((item) => (
          <a key={item} href="#" className="top-nav__link">
            {item}
          </a>
        ))}
      </div>
    </nav>
  )
}
```

===FILE: src/components/TopNav.css===
```css
.top-nav {
  width: 100%;
  padding: 18px 24px 0;
  box-sizing: border-box;
}

.top-nav__links {
  display: flex;
  align-items: center;
  gap: 22px;
  flex-wrap: wrap;
}

.top-nav__link {
  color: #222;
  font-size: 14px;
  text-decoration: none;
  font-family: 'PingFang SC', Arial, sans-serif;
}

.top-nav__link:hover {
  color: #4e6ef2;
  text-decoration: underline;
}
```

===FILE: src/components/Logo.tsx===
```tsx
import './Logo.css'

export default function Logo() {
  return (
    <div className="logo">
      <span className="logo__bai">Bai</span>
      <span className="logo__du">du</span>
      <span className="logo__cn">百度</span>
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
  user-select: none;
  margin-bottom: 22px;
}

.logo__bai {
  font-size: 44px;
  color: #2932e1;
  letter-spacing: -1px;
}

.logo__du {
  font-size: 44px;
  color: #4e6ef2;
  letter-spacing: -1px;
}

.logo__cn {
  font-size: 44px;
  color: #2932e1;
  margin-left: 4px;
}
```

===FILE: src/components/SearchBox.tsx===
```tsx
import './SearchBox.css'

interface SearchBoxProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
}

export default function SearchBox({ value, onChange, onSubmit }: SearchBoxProps) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      onSubmit()
    }
  }

  return (
    <div className="search-box">
      <div className="search-box__field">
        <textarea
          data-testid="search-input"
          className="search-box__input"
          placeholder="演员刘洵去世"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
        />
        <div className="search-box__tools">
          <button className="search-box__tool" type="button" title="语音">
            <MicIcon />
          </button>
          <button className="search-box__tool" type="button" title="附件">
            <ClipIcon />
          </button>
          <button className="search-box__tool" type="button" title="图片">
            <ImageIcon />
          </button>
          <button
            data-testid="search-button"
            className="search-box__submit"
            type="button"
            onClick={onSubmit}
          >
            百度一下
          </button>
        </div>
      </div>
    </div>
  )
}

function MicIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#878a99" strokeWidth="2">
      <rect x="9" y="3" width="6" height="11" rx="3" />
      <path d="M5 11a7 7 0 0 0 14 0" />
      <line x1="12" y1="18" x2="12" y2="21" />
    </svg>
  )
}

function ClipIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#878a99" strokeWidth="2">
      <path d="M21 11.5l-8.5 8.5a5 5 0 0 1-7-7l8.5-8.5a3.5 3.5 0 0 1 5 5l-8.5 8.5a2 2 0 0 1-3-3l8-8" />
    </svg>
  )
}

function ImageIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#878a99" strokeWidth="2">
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <circle cx="8.5" cy="9.5" r="1.5" />
      <path d="M21 16l-5-5L5 20" />
    </svg>
  )
}
```

===FILE: src/components/SearchBox.css===
```css
.search-box {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.search-box__field {
  position: relative;
  border: 1px solid #4e6ef2;
  border-radius: 12px;
  padding: 16px 18px 56px;
  box-shadow: 0 2px 10px rgba(78, 110, 242, 0.08);
  background: #fff;
}

.search-box__input {
  width: 100%;
  border: none;
  outline: none;
  resize: none;
  font-size: 16px;
  line-height: 22px;
  color: #222;
  font-family: 'PingFang SC', Arial, sans-serif;
  background: transparent;
  min-height: 22px;
  overflow: hidden;
}

.search-box__input::placeholder {
  color: #9195a3;
}

.search-box__tools {
  position: absolute;
  right: 14px;
  bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-box__tool {
  width: 34px;
  height: 34px;
  border: none;
  background: transparent;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.search-box__tool:hover {
  background: #f1f3ff;
}

.search-box__submit {
  margin-left: 8px;
  height: 40px;
  padding: 0 26px;
  border: none;
  border-radius: 10px;
  background: #4e6ef2;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  font-family: 'PingFang SC', Arial, sans-serif;
  transition: background 0.15s;
}

.search-box__submit:hover {
  background: #4156d6;
}
```

===FILE: src/components/HotSearch.tsx===
```tsx
import { hotList } from '../data/mock'
import './HotSearch.css'

interface HotSearchProps {
  onItemClick: (text: string) => void
}

export default function HotSearch({ onItemClick }: HotSearchProps) {
  return (
    <section className="hot-search">
      <div className="hot-search__head">
        <span className="hot-search__title">
          百度<span className="hot-search__title-accent">热搜</span>
          <span className="hot-search__arrow">›</span>
        </span>
        <button className="hot-search__refresh" type="button">
          <RefreshIcon /> 换一换
        </button>
      </div>
      <ul className="hot-search__list">
        {hotList.map((item, index) => (
          <li key={item.id} className="hot-search__item">
            <button
              className="hot-search__entry"
              type="button"
              onClick={() => onItemClick(item.text)}
            >
              <span className={`hot-search__rank rank-${index + 1}`}>
                {index + 1}
              </span>
              <span className="hot-search__text">{item.text}</span>
              {item.tag && (
                <span className={`hot-search__tag tag--${item.tag}`}>
                  {item.tag === 'hot' ? '热' : '新'}
                </span>
              )}
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}

function RefreshIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 12a9 9 0 1 1-2.64-6.36" />
      <path d="M21 3v6h-6" />
    </svg>
  )
}
```

===FILE: src/components/HotSearch.css===
```css
.hot-search {
  width: 100%;
  max-width: 800px;
  margin: 40px auto 0;
}

.hot-search__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.hot-search__title {
  font-size: 18px;
  font-weight: 700;
  color: #222;
  display: inline-flex;
  align-items: center;
}

.hot-search__title-accent {
  color: #4e6ef2;
}

.hot-search__arrow {
  color: #9195a3;
  margin-left: 6px;
  font-weight: 400;
}

.hot-search__refresh {
  border: none;
  background: transparent;
  color: #9195a3;
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.hot-search__refresh:hover {
  color: #4e6ef2;
}

.hot-search__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 40px;
}

.hot-search__item {
  border-radius: 6px;
}

.hot-search__entry {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  text-align: left;
  border-radius: 6px;
}

.hot-search__entry:hover {
  background: #f6f7fe;
}

.hot-search__rank {
  width: 18px;
  text-align: center;
  font-size: 14px;
  color: #9195a3;
  flex-shrink: 0;
  font-family: Arial, sans-serif;
}

.hot-search__rank.rank-1 { color: #fe2d46; }
.hot-search__rank.rank-2 { color: #f60; }
.hot-search__rank.rank-3 { color: #ff9406; }

.hot-search__text {
  font-size: 14px;
  color: #222;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hot-search__entry:hover .hot-search__text {
  color: #4e6ef2;
}

.hot-search__tag {
  font-size: 12px;
  color: #fff;
  border-radius: 3px;
  padding: 1px 5px;
  flex-shrink: 0;
}

.tag--hot {
  background: #ff5b00;
}

.tag--new {
  background: #fe2d46;
}
```

===FILE: src/components/SearchResults.tsx===
```tsx
import type { SearchResult } from '../data/mock'
import './SearchResults.css'

interface SearchResultsProps {
  keyword: string
  results: SearchResult[]
  totalCount: number
  page: number
  totalPages: number
  onNextPage: () => void
  onPrevPage: () => void
}

export default function SearchResults({
  keyword,
  results,
  totalCount,
  page,
  totalPages,
  onNextPage,
  onPrevPage,
}: SearchResultsProps) {
  return (
    <section className="results">
      <div className="results__meta">
        关于 <span className="results__keyword">{keyword}</span> 的搜索结果约
        {' '}{totalCount.toLocaleString()} 个
      </div>

      <ul className="results__list" data-testid="result-list">
        {results.map((item) => (
          <li key={item.id} className="results__item">
            <h3 className="results__title">
              <a href="#" onClick={(e) => e.preventDefault()}>
                {item.title}
              </a>
            </h3>
            <div className="results__source">{item.source}</div>
            <p className="results__abstract">{item.abstract}</p>
          </li>
        ))}
      </ul>

      <div className="results__pagination">
        <button
          className="results__page-btn"
          type="button"
          onClick={onPrevPage}
          disabled={page <= 1}
        >
          上一页
        </button>
        <span className="results__page-info">
          第 {page} / {totalPages} 页
        </span>
        <button
          data-testid="next-page"
          className="results__page-btn results__page-btn--next"
          type="button"
          onClick={onNextPage}
          disabled={page >= totalPages}
        >
          下一页 ›
        </button>
      </div>
    </section>
  )
}
```

===FILE: src/components/SearchResults.css===
```css
.results {
  width: 100%;
  max-width: 800px;
  margin: 24px auto 0;
  text-align: left;
}

.results__meta {
  font-size: 13px;
  color: #9195a3;
  margin-bottom: 18px;
}

.results__keyword {
  color: #fe2d46;
}

.results__list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.results__item {
  margin-bottom: 22px;
}

.results__title {
  margin: 0 0 4px;
  font-size: 18px;
  font-weight: 400;
  line-height: 1.4;
}

.results__title a {
  color: #2440b3;
  text-decoration: none;
}

.results__title a:hover {
  text-decoration: underline;
}

.results__source {
  font-size: 13px;
  color: #9195a3;
  margin-bottom: 4px;
}

.results__abstract {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

.results__pagination {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 30px 0 40px;
}

.results__page-btn {
  padding: 7px 18px;
  border: 1px solid #e0e3eb;
  border-radius: 8px;
  background: #fff;
  color: #4e6ef2;
  font-size: 14px;
  cursor: pointer;
  font-family: 'PingFang SC', Arial, sans-serif;
}

.results__page-btn:hover:not(:disabled) {
  border-color: #4e6ef2;
  background: #f6f7fe;
}

.results__page-btn:disabled {
  color: #bbb;
  cursor: not-allowed;
  border-color: #eee;
}

.results__page-btn--next {
  background: #4e6ef2;
  color: #fff;
  border-color: #4e6ef2;
}

.results__page-btn--next:hover:not(:disabled) {
  background: #4156d6;
}

.results__page-btn--next:disabled {
  background: #c4cdf7;
  color: #fff;
  border-color: #c4cdf7;
}

.results__page-info {
  font-size: 13px;
  color: #333;
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

const records = [
  '京公网安备11000002000001号',
  '京ICP证030173号',
  '互联网新闻信息服务许可11220180008',
  '网络文化经营许可证：京网文〔2026〕0171-042号',
]

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer__links">
        {links.map((link) => (
          <a key={link} href="#" className="footer__link">
            {link}
          </a>
        ))}
      </div>
      <div className="footer__records">
        {records.map((rec) => (
          <span key={rec} className="footer__record">
            {rec}
          </span>
        ))}
      </div>
    </footer>
  )
}
```

===FILE: src/components/Footer.css===
```css
.footer {
  margin-top: auto;
  padding: 18px 24px;
  border-top: 1px solid #f1f1f1;
  text-align: center;
}

.footer__links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  margin-bottom: 8px;
}

.footer__link {
  color: #9195a3;
  font-size: 12px;
  text-decoration: none;
}

.footer__link:hover {
  color: #4e6ef2;
  text-decoration: underline;
}

.footer__records {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 14px;
}

.footer__record {
  color: #bbb;
  font-size: 12px;
}
```

===FILE: src/data/mock.ts===
```ts
export interface HotItem {
  id: number
  text: string
  tag?: 'hot' | 'new'
}

export interface SearchResult {
  id: number
  title: string
  source: string
  abstract: string
}

export const hotList: HotItem[] = [
  { id: 1, text: '加快高水平科技自立自强' },
  { id: 2, text: '湖北一社区书记多看一眼救下128人', tag: 'new' },
  { id: 3, text: '印政府警告宝莱坞：不得�researchsm抨击中国', tag: 'hot' },
  { id: 4, text: '国家首次专门发文 这四类人群受益' },
  { id: 5, text: '车手张秀军意外离世 留下3个孩子', tag: 'new' },
  { id: 6, text: '中国公民在菲监狱离世 中方严正交涉' },
  { id: 7, text: '老人与邻居互殴次日自缢 法院判了' },
  { id: 8, text: '演员刘洵去世 曾参演《九品芝麻官》', tag: 'new' },
  { id: 9, text: '17岁女生打赏650万 起诉退款被驳回' },
  { id: 10, text: '市民打12345求干预天气 当地回应', tag: 'hot' },
]

const sources = [
  '百度百科',
  '新华网',
  '人民网',
  '澎湃新闻',
  '中国新闻网',
  '腾讯网',
  '知乎',
  '微博',
  '搜狐网',
  '网易新闻',
  '今日头条',
  '央视新闻',
]

export function searchMock(keyword: string): SearchResult[] {
  const templates = [
    `${keyword}_百度百科。${keyword}是近期备受关注的话题，本词条详细介绍了${keyword}的背景、发展过程以及相关的重要信息，帮助你快速全面了解${keyword}的来龙去脉。`,
    `关于${keyword}的最新报道：多家媒体对${keyword}进行了跟踪报道，事件持续引发社会广泛讨论，相关部门已作出回应，更多细节正在进一步核实中。`,
    `${keyword}相关专题汇总。这里收录了${keyword}的全部资讯、深度分析与网友热评，从不同角度解读${keyword}背后的故事与意义。`,
    `${keyword}是什么意思？本文从多个维度解析${keyword}的含义与影响，结合实际案例为你梳理${keyword}的关键要点和常见疑问。`,
    `${keyword}_知乎讨论。超过千名网友参与了关于${keyword}的话题讨论，高赞回答从专业角度分享了对${keyword}的独到见解。`,
    `${keyword}最新进展与时间线梳理。我们按时间顺序整理了${keyword}事件的每一个关键节点，让你一目了然掌握${keyword}的来龙去脉。`,
    `${keyword}图片大全 - 高清图集。精选与${keyword}相关的高清图片，涵盖多个场景与角度，为你呈现${keyword}的真实面貌。`,
    `${keyword}官方信息发布。权威渠道关于${keyword}的正式声明和说明，内容真实可靠，建议以官方发布为准。`,
    `${keyword}背后的真相到底是什么？深度调查报道还原${keyword}事件全貌，多方采访带你看清${keyword}的本质。`,
    `${keyword}相关视频 - 在线观看。汇集${keyword}的精彩视频内容，包括现场画面、专家解读和网友热议，全方位记录${keyword}。`,
    `${keyword}热议持续发酵 网友评论两极分化。围绕${keyword}的讨论在社交平台上引发热潮，不同观点激烈交锋。`,
    `${keyword}全解析：一文读懂${keyword}。从起因到影响，从数据到观点，本文系统梳理了${keyword}的方方面面。`,
  ]

  return templates.map((abstract, index) => ({
    id: index + 1,
    title: `${keyword} - ${sources[index % sources.length]}`,
    source: `${sources[index % sources.length]}  ·  ${index + 1}小时前`,
    abstract,
  }))
}
```

===FILE: src/styles/global.css===
```css
* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
}

body {
  font-family: 'PingFang SC', Arial, sans-serif;
  color: #222;
  background: #fff;
  -webkit-font-smoothing: antialiased;
}

a {
  color: inherit;
}

#root {
  min-height: 100vh;
}
```

===FILE: src/styles/app.css===
```css
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main {
  flex: 1;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.main:not(.main--searched) {
  padding-top: 90px;
}

.main--searched {
  padding-top: 36px;
  align-items: stretch;
}

.wenxin-banner {
  margin: 26px auto 0;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #545970;
  background: #f6f7fe;
  border-radius: 18px;
  padding: 8px 18px;
}

.wenxin-icon {
  background: linear-gradient(135deg, #4e6ef2, #6a5cff);
  color: #fff;
  font-size: 12px;
  border-radius: 10px;
  padding: 2px 8px;
}

.wenxin-arrow {
  color: #9195a3;
}
```