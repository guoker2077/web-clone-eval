===FILE: package.json===
```json
{
  "name": "baidu-homepage-clone",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "typescript": "^5.5.3",
    "vite": "^5.3.4"
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
    "noUnusedLocals": true,
    "noUnusedParameters": true,
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
    "strict": true
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
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
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
  background-color: #fff;
  -webkit-font-smoothing: antialiased;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  font-family: inherit;
  cursor: pointer;
}

input,
textarea {
  font-family: inherit;
  outline: none;
  border: none;
}
```

===FILE: src/data/mock.ts===
```ts
export interface SearchResult {
  id: string
  title: string
  summary: string
  source: string
  date: string
  url: string
}

const summaryTemplates = [
  '关于“{kw}”的最新资讯与详细介绍，涵盖背景、发展与相关动态，帮助你快速了解全貌。',
  '{kw} 的百科解释、相关词条与延伸阅读，收录权威资料与网友讨论内容。',
  '本页汇总了 {kw} 的热门话题、图片、视频以及实时更新的相关新闻报道。',
  '查找 {kw} 相关的产品、服务与教程，提供多角度的解读和实用参考信息。',
  '{kw} 怎么样？看看大家都在讨论什么，这里有最全面的观点汇总与评测分析。',
  '权威机构与媒体对 {kw} 的报道集合，包含数据统计、专家观点与深度分析。',
  '{kw} 入门指南：从基础概念到进阶技巧，一文带你全面掌握相关知识要点。',
  '网友热议 {kw}，相关问答、经验分享与常见问题解答，助你少走弯路。',
]

const sources = [
  '百度百科',
  '新华网',
  '人民网',
  '知乎',
  '搜狐网',
  '腾讯网',
  '今日头条',
  '中国新闻网',
  '澎湃新闻',
  '百度知道',
]

function pad(n: number): string {
  return n < 10 ? `0${n}` : `${n}`
}

function dateForIndex(index: number): string {
  const base = new Date(2024, 0, 1)
  base.setDate(base.getDate() - index * 3)
  return `${base.getFullYear()}-${pad(base.getMonth() + 1)}-${pad(base.getDate())}`
}

const PAGE_SIZE = 10

export function getResults(keyword: string, page: number): SearchResult[] {
  const kw = keyword.trim()
  const start = (page - 1) * PAGE_SIZE
  const results: SearchResult[] = []
  for (let i = 0; i < PAGE_SIZE; i++) {
    const globalIndex = start + i
    const summary = summaryTemplates[globalIndex % summaryTemplates.length].replace(
      /\{kw\}/g,
      kw,
    )
    results.push({
      id: `${kw}-${globalIndex}`,
      title: `${kw}${globalIndex === 0 ? '' : '_'}${globalIndex === 0 ? '' : '相关结果 ' + (globalIndex + 1)}${globalIndex === 0 ? ' - 百度搜索' : ''}`.trim() || kw,
      summary,
      source: sources[globalIndex % sources.length],
      date: dateForIndex(globalIndex),
      url: `https://www.baidu.com/s?wd=${encodeURIComponent(kw)}&pn=${globalIndex}`,
    })
  }
  return results
}

export const RESULTS_PER_PAGE = PAGE_SIZE
export const TOTAL_PAGES = 10

export const topNav = [
  '新闻',
  'hao123',
  '地图',
  '贴吧',
  '视频',
  '图片',
  '网盘',
  '文库',
  '关于DuMate',
  '设置',
]

export interface HotItem {
  rank: number
  text: string
  hot?: boolean
}

export const hotSearch: HotItem[] = [
  { rank: 0, text: '坚持高质量发展是硬道理' },
  { rank: 1, text: '我国有了“太空粮仓”', hot: true },
  { rank: 2, text: '14条措施支持民营经济 提振发展信心' },
  { rank: 3, text: '把绿水青山 转化为金山银山' },
  { rank: 4, text: '“数字中国 加速跑”', hot: true },
  { rank: 5, text: '消费市场持续回暖向好', hot: true },
  { rank: 6, text: '科技自立自强 迈出坚实步伐', hot: true },
  { rank: 7, text: '一组数据200余 看经济运行态势' },
  { rank: 8, text: '春耕备耕忙起来 农业生产开局良好', hot: true },
  { rank: 9, text: '乡村振兴绘就壮美新画卷' },
]
```

===FILE: src/components/Icons.tsx===
```tsx
export function MicIcon() {
  return (
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#666" strokeWidth="1.6">
      <rect x="9" y="3" width="6" height="11" rx="3" />
      <path d="M6 11a6 6 0 0 0 12 0" />
      <line x1="12" y1="17" x2="12" y2="21" />
      <line x1="9" y1="21" x2="15" y2="21" />
    </svg>
  )
}

export function ClipIcon() {
  return (
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#666" strokeWidth="1.6">
      <path d="M21 11.5 12.5 20a5 5 0 0 1-7-7l8-8a3.5 3.5 0 0 1 5 5l-8 8a2 2 0 0 1-3-3l7.5-7.5" />
    </svg>
  )
}

export function ImageIcon() {
  return (
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#666" strokeWidth="1.6">
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <circle cx="8.5" cy="9.5" r="1.8" />
      <path d="m4 18 5-5 4 4 3-3 4 4" />
    </svg>
  )
}

export function RefreshIcon() {
  return (
    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#9195a3" strokeWidth="2">
      <path d="M4 12a8 8 0 0 1 13.7-5.7L20 8" />
      <path d="M20 4v4h-4" />
      <path d="M20 12a8 8 0 0 1-13.7 5.7L4 16" />
      <path d="M4 20v-4h4" />
    </svg>
  )
}
```

===FILE: src/App.tsx===
```tsx
import { useMemo, useState } from 'react'
import './App.css'
import {
  getResults,
  hotSearch,
  topNav,
  TOTAL_PAGES,
  type SearchResult,
} from './data/mock'
import { ClipIcon, ImageIcon, MicIcon, RefreshIcon } from './components/Icons'

function rankColor(rank: number): string {
  if (rank === 0) return '#fe2d46'
  if (rank === 1) return '#f60'
  if (rank === 2) return '#ff8547'
  return '#999'
}

export default function App() {
  const [input, setInput] = useState('')
  const [keyword, setKeyword] = useState('')
  const [page, setPage] = useState(1)
  const [searched, setSearched] = useState(false)

  const results: SearchResult[] = useMemo(() => {
    if (!searched || !keyword) return []
    return getResults(keyword, page)
  }, [searched, keyword, page])

  const runSearch = (term: string) => {
    const value = term.trim()
    if (!value) return
    setKeyword(value)
    setPage(1)
    setSearched(true)
  }

  const handleSubmit = () => runSearch(input)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleSubmit()
    }
  }

  const goToPage = (next: number) => {
    if (next < 1 || next > TOTAL_PAGES) return
    setPage(next)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="page">
      <header className="top-nav">
        <nav className="top-nav-links">
          {topNav.map((item) => (
            <a key={item} href="#" className="top-nav-link">
              {item}
            </a>
          ))}
        </nav>
      </header>

      <main className="main">
        <div className="logo">
          <span className="logo-bai">Bai</span>
          <span className="logo-du">du</span>
          <span className="logo-cn">百度</span>
        </div>

        <div className="search-box">
          <textarea
            className="search-input"
            data-testid="search-input"
            placeholder="百度一下，你就知道"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          <div className="search-tools">
            <button className="tool-btn" title="语音" type="button">
              <MicIcon />
            </button>
            <button className="tool-btn" title="附件" type="button">
              <ClipIcon />
            </button>
            <button className="tool-btn" title="图片" type="button">
              <ImageIcon />
            </button>
            <button
              className="search-button"
              data-testid="search-button"
              type="submit"
              onClick={handleSubmit}
            >
              百度一下
            </button>
          </div>
        </div>

        <div className="wenxin-banner">
          <span className="wenxin-logo">文心</span>
          <span className="wenxin-text">免费体验文心一言，开启你的智能助手之旅</span>
          <span className="wenxin-arrow">›</span>
        </div>

        {!searched ? (
          <section className="hot-search">
            <div className="hot-head">
              <div className="hot-title">
                百度<span className="hot-title-accent">热搜</span> ›
              </div>
              <div className="hot-refresh">
                <RefreshIcon /> 换一换
              </div>
            </div>
            <ol className="hot-list">
              {hotSearch.map((item) => (
                <li key={item.rank} className="hot-item">
                  <button
                    type="button"
                    className="hot-link"
                    onClick={() => {
                      setInput(item.text)
                      runSearch(item.text)
                    }}
                  >
                    <span
                      className="hot-rank"
                      style={{ color: rankColor(item.rank) }}
                    >
                      {item.rank === 0 ? '不' : item.rank}
                    </span>
                    <span className="hot-text">{item.text}</span>
                    {item.hot && <span className="hot-tag">热</span>}
                  </button>
                </li>
              ))}
            </ol>
          </section>
        ) : (
          <section className="results">
            <div className="results-meta">
              搜索 <strong>{keyword}</strong> 找到约 1,250,000 个结果（第 {page} 页）
            </div>
            <ul className="result-list" data-testid="result-list">
              {results.map((r) => (
                <li key={r.id} className="result-item">
                  <a href={r.url} className="result-title" onClick={(e) => e.preventDefault()}>
                    {r.title}
                  </a>
                  <p className="result-summary">{r.summary}</p>
                  <div className="result-foot">
                    <span className="result-source">{r.source}</span>
                    <span className="result-date">{r.date}</span>
                  </div>
                </li>
              ))}
            </ul>

            <div className="pagination" data-testid="pagination">
              <button
                className="page-btn"
                data-testid="prev-page"
                onClick={() => goToPage(page - 1)}
                disabled={page <= 1}
              >
                上一页
              </button>
              <span className="page-indicator">
                第 {page} / {TOTAL_PAGES} 页
              </span>
              <button
                className="page-btn next"
                data-testid="next-page"
                onClick={() => goToPage(page + 1)}
                disabled={page >= TOTAL_PAGES}
              >
                下一页
              </button>
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <div className="footer-links">
          <a href="#">设为首页</a>
          <a href="#">About Baidu</a>
          <a href="#">百度营销</a>
          <a href="#">使用百度前必读</a>
          <a href="#">意见反馈</a>
          <span>京公网安备11000002000001号</span>
          <span>京ICP证030173号</span>
        </div>
      </footer>
    </div>
  )
}
```

===FILE: src/App.css===
```css
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #fff;
}

/* Top navigation */
.top-nav {
  width: 100%;
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.top-nav-links {
  display: flex;
  gap: 26px;
  align-items: center;
}

.top-nav-link {
  font-size: 14px;
  color: #222;
}

.top-nav-link:hover {
  color: #4e6ef2;
}

/* Main */
.main {
  flex: 1;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 16px 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Logo */
.logo {
  font-family: Arial, sans-serif;
  font-weight: 700;
  font-size: 56px;
  letter-spacing: -1px;
  margin: 30px 0 36px;
  display: flex;
  align-items: baseline;
}

.logo-bai {
  color: #4e6ef2;
}

.logo-du {
  color: #f73131;
}

.logo-cn {
  color: #4e6ef2;
  font-size: 52px;
  margin-left: 2px;
}

/* Search box */
.search-box {
  width: 100%;
  border: 2px solid #4e6ef2;
  border-radius: 14px;
  padding: 16px 18px 12px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(78, 110, 242, 0.08);
}

.search-input {
  width: 100%;
  font-size: 16px;
  color: #222;
  line-height: 1.4;
  resize: none;
  min-height: 28px;
  background: transparent;
}

.search-input::placeholder {
  color: #9195a3;
}

.search-tools {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14px;
  margin-top: 18px;
}

.tool-btn {
  width: 34px;
  height: 34px;
  border: none;
  background: transparent;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-btn:hover {
  background: #f6f7fe;
}

.search-button {
  margin-left: 8px;
  height: 44px;
  padding: 0 26px;
  border: none;
  border-radius: 22px;
  color: #fff;
  font-size: 16px;
  background: linear-gradient(90deg, #4e6ef2, #5a7bff);
  transition: filter 0.15s;
}

.search-button:hover {
  filter: brightness(1.05);
}

/* Wenxin banner */
.wenxin-banner {
  margin-top: 28px;
  height: 44px;
  padding: 0 18px;
  background: #f6f7fe;
  border-radius: 22px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.wenxin-logo {
  font-size: 13px;
  color: #4e6ef2;
  background: #e8ecff;
  border-radius: 12px;
  padding: 3px 10px;
}

.wenxin-text {
  font-size: 14px;
  color: #333;
}

.wenxin-arrow {
  color: #9195a3;
  font-size: 18px;
}

/* Hot search */
.hot-search {
  width: 100%;
  margin-top: 40px;
}

.hot-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.hot-title {
  font-size: 18px;
  font-weight: 700;
  color: #222;
}

.hot-title-accent {
  color: #f73131;
}

.hot-refresh {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #9195a3;
  cursor: pointer;
}

.hot-list {
  list-style: none;
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 50px;
  row-gap: 8px;
}

.hot-item {
  display: flex;
}

.hot-link {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  background: transparent;
  border: none;
  padding: 6px 4px;
  text-align: left;
  border-radius: 6px;
}

.hot-link:hover {
  background: #f6f7fe;
}

.hot-link:hover .hot-text {
  color: #4e6ef2;
}

.hot-rank {
  width: 18px;
  font-size: 15px;
  font-weight: 700;
  text-align: center;
  flex-shrink: 0;
}

.hot-text {
  font-size: 15px;
  color: #222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hot-tag {
  font-size: 11px;
  color: #fff;
  background: #fe2d46;
  border-radius: 3px;
  padding: 1px 4px;
  flex-shrink: 0;
}

/* Results */
.results {
  width: 100%;
  margin-top: 36px;
  align-self: flex-start;
}

.results-meta {
  font-size: 13px;
  color: #9195a3;
  margin-bottom: 18px;
}

.results-meta strong {
  color: #4e6ef2;
}

.result-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 26px;
}

.result-item {
  max-width: 700px;
}

.result-title {
  font-size: 18px;
  color: #0000ee;
  line-height: 1.4;
}

.result-title:hover {
  text-decoration: underline;
}

.result-summary {
  font-size: 14px;
  color: #333;
  line-height: 1.7;
  margin-top: 6px;
}

.result-foot {
  display: flex;
  gap: 14px;
  margin-top: 8px;
  font-size: 13px;
  color: #9195a3;
}

.result-source {
  color: #4e6ef2;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 40px;
}

.page-btn {
  min-width: 84px;
  height: 38px;
  border: 1px solid #e0e3ee;
  background: #fff;
  border-radius: 8px;
  font-size: 14px;
  color: #4e6ef2;
}

.page-btn:hover:not(:disabled) {
  border-color: #4e6ef2;
  background: #f6f7fe;
}

.page-btn:disabled {
  color: #bbb;
  cursor: not-allowed;
}

.page-indicator {
  font-size: 14px;
  color: #333;
}

/* Footer */
.footer {
  border-top: 1px solid #f1f1f1;
  padding: 18px 16px;
  background: #fbfbfb;
}

.footer-links {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 12px;
  color: #9195a3;
  justify-content: center;
}

.footer-links a:hover {
  color: #4e6ef2;
}
```