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
    "strict": true,
    "noEmit": true
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
  color: rgb(34, 34, 34);
  background: #fff;
  -webkit-font-smoothing: antialiased;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  background: none;
}

input,
textarea {
  font-family: inherit;
  outline: none;
  border: none;
}
```

===FILE: src/App.tsx===
```tsx
import { useState, useRef, type FormEvent } from 'react'
import './App.css'
import { generateResults, type SearchResult, PAGE_SIZE } from './mock'

const NAV_LINKS = [
  '新闻',
  'hao123',
  '地图',
  '贴吧',
  '视频',
  '图片',
  '网盘',
  '文库',
  '更多DuMate',
]

const HOT_SEARCH = [
  { rank: '', label: '坚定不移推动经济社会高质量发展', hot: false },
  { rank: '1', label: '一组数据看“十四五”', tag: 'hot' },
  { rank: '2', label: '14年前的今天我们永远铭记', tag: '' },
  { rank: '3', label: '走进博物馆 触摸历史的温度', tag: '' },
  { rank: '4', label: '“真主党 不会缴械”', tag: 'new' },
  { rank: '5', label: '秋日里的丰收画卷', tag: 'hot' },
  { rank: '6', label: '多地推出政策 促进消费持续升温', tag: 'rec' },
  { rank: '7', label: '减重200斤 他重启人生', tag: '' },
  { rank: '8', label: '科技创新引领新质生产力发展', tag: 'rec' },
  { rank: '9', label: '金秋时节话丰收说振兴', tag: '' },
]

export default function App() {
  const [keyword, setKeyword] = useState('')
  const [submittedKeyword, setSubmittedKeyword] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [page, setPage] = useState(1)
  const [searched, setSearched] = useState(false)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const runSearch = (kw: string, targetPage: number) => {
    const trimmed = kw.trim()
    if (!trimmed) return
    const data = generateResults(trimmed, targetPage)
    setResults(data)
    setSubmittedKeyword(trimmed)
    setPage(targetPage)
    setSearched(true)
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    runSearch(keyword, 1)
  }

  const goNextPage = () => {
    runSearch(submittedKeyword, page + 1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const goPrevPage = () => {
    if (page <= 1) return
    runSearch(submittedKeyword, page - 1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className={`page ${searched ? 'page--results' : ''}`}>
      <header className="topnav">
        <nav className="topnav__links">
          {NAV_LINKS.map((l) => (
            <a key={l} href="#" className="topnav__link">
              {l}
            </a>
          ))}
        </nav>
        <div className="topnav__right">
          <a href="#" className="topnav__link">
            设置
          </a>
          <button className="topnav__login">登录</button>
        </div>
      </header>

      <main className="main">
        <div className={`brand ${searched ? 'brand--small' : ''}`}>
          <span className="brand__bai">Bai</span>
          <span className="brand__du">du</span>
          <span className="brand__cn">百度</span>
        </div>

        <form className="searchbox" onSubmit={handleSubmit}>
          <textarea
            ref={inputRef}
            data-testid="search-input"
            className="searchbox__input"
            placeholder="今天你想了解点什么7呢？"
            value={keyword}
            rows={searched ? 1 : 3}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                runSearch(keyword, 1)
              }
            }}
          />
          <div className="searchbox__toolbar">
            <div className="searchbox__icons">
              <span className="searchbox__icon" title="语音">
                🎤
              </span>
              <span className="searchbox__icon" title="附件">
                📎
              </span>
              <span className="searchbox__icon" title="图片">
                🖼️
              </span>
            </div>
            <button
              type="submit"
              data-testid="search-button"
              className="searchbox__btn"
            >
              百度一下
            </button>
          </div>
        </form>

        {!searched && (
          <>
            <div className="wenxin">
              <span className="wenxin__icon">文心</span>
              <span className="wenxin__text">
                文心大模型已升级，体验更智能的对话与创作
              </span>
              <span className="wenxin__arrow">›</span>
            </div>

            <section className="hot">
              <div className="hot__header">
                <span className="hot__title">
                  百度热<span className="hot__title-accent">搜</span>
                </span>
                <span className="hot__refresh">↻ 换一换</span>
              </div>
              <ul className="hot__list">
                {HOT_SEARCH.map((item, i) => (
                  <li
                    key={i}
                    className="hot__item"
                    onClick={() => {
                      setKeyword(item.label)
                      runSearch(item.label, 1)
                    }}
                  >
                    <span
                      className={`hot__rank hot__rank--${
                        i < 3 ? 'top' : 'normal'
                      }`}
                    >
                      {item.rank || '丆'}
                    </span>
                    <span className="hot__label">{item.label}</span>
                    {item.tag === 'hot' && (
                      <span className="hot__tag hot__tag--hot">热</span>
                    )}
                    {item.tag === 'new' && (
                      <span className="hot__tag hot__tag--new">新</span>
                    )}
                    {item.tag === 'rec' && (
                      <span className="hot__tag hot__tag--rec">荐</span>
                    )}
                  </li>
                ))}
              </ul>
            </section>
          </>
        )}

        {searched && (
          <section className="results">
            <div className="results__meta">
              搜索 <strong>{submittedKeyword}</strong> 的相关结果，第 {page} 页
            </div>
            <ul className="results__list" data-testid="result-list">
              {results.map((r) => (
                <li key={r.id} className="result">
                  <a href="#" className="result__title">
                    {r.title}
                  </a>
                  <div className="result__url">{r.url}</div>
                  <p className="result__summary">{r.summary}</p>
                </li>
              ))}
            </ul>

            <div className="pagination" data-testid="pagination">
              <button
                className="pagination__btn"
                data-testid="prev-page"
                disabled={page <= 1}
                onClick={goPrevPage}
              >
                上一页
              </button>
              <span className="pagination__page">第 {page} 页</span>
              <button
                className="pagination__btn pagination__btn--next"
                data-testid="next-page"
                onClick={goNextPage}
              >
                下一页 ›
              </button>
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <div className="footer__links">
          <a href="#">关于百度</a>
          <a href="#">About Baidu</a>
          <a href="#">使用百度前必读</a>
          <a href="#">意见反馈</a>
          <a href="#">帮助中心</a>
          <span>京公网安备11000002000001号</span>
          <span>京ICP证030173号</span>
        </div>
      </footer>
    </div>
  )
}
```

===FILE: src/mock.ts===
```ts
export interface SearchResult {
  id: number
  title: string
  url: string
  summary: string
}

export const PAGE_SIZE = 10

const TITLE_TEMPLATES = [
  '{kw}_百度百科',
  '{kw}最新资讯_{kw}相关报道汇总',
  '关于{kw}你需要知道的几件事',
  '{kw}是什么意思？{kw}的含义与用法',
  '{kw}官方网站 - 权威信息发布',
  '{kw}深度解析：发展现状与未来趋势',
  '一文读懂{kw}的来龙去脉',
  '{kw}相关问题解答 - 知道',
  '{kw}图片大全_高清{kw}素材下载',
  '{kw}最新进展与热点追踪',
]

const SUMMARY_TEMPLATES = [
  '关于"{kw}"的详细介绍，涵盖基本概念、背景知识与常见问题，帮助你快速全面地了解相关内容。',
  '本页汇总了"{kw}"的最新动态与权威解读，内容持续更新，为你提供准确可靠的参考信息。',
  '为你整理"{kw}"的核心要点与实用资料，包含案例分析与专家观点，深入浅出便于理解。',
  '"{kw}"相关搜索结果，包括定义、发展历程、应用场景等多方面内容，满足你的查询需求。',
  '这里有海量与"{kw}"相关的图文、视频与资讯，全方位呈现你关心的话题，点击查看更多。',
]

export function generateResults(
  keyword: string,
  page: number,
  pageSize: number = PAGE_SIZE,
): SearchResult[] {
  const results: SearchResult[] = []
  for (let i = 0; i < pageSize; i++) {
    const index = (page - 1) * pageSize + i
    const title = TITLE_TEMPLATES[index % TITLE_TEMPLATES.length].replace(
      /{kw}/g,
      keyword,
    )
    const summary = SUMMARY_TEMPLATES[index % SUMMARY_TEMPLATES.length].replace(
      /{kw}/g,
      keyword,
    )
    results.push({
      id: index + 1,
      title,
      url: `https://www.baidu.com/s?wd=${encodeURIComponent(
        keyword,
      )}&pn=${index}`,
      summary,
    })
  }
  return results
}
```

===FILE: src/App.css===
```css
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ===== Top nav ===== */
.topnav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 44px;
}

.topnav__links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.topnav__link {
  font-size: 13px;
  color: rgb(34, 34, 34);
}

.topnav__link:hover {
  color: rgb(78, 110, 242);
}

.topnav__right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.topnav__login {
  font-size: 13px;
  color: #fff;
  background: rgb(78, 110, 242);
  padding: 6px 16px;
  border-radius: 16px;
}

/* ===== Main ===== */
.main {
  flex: 1;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page:not(.page--results) .main {
  padding-top: 60px;
}

.page--results .main {
  padding-top: 24px;
  align-items: stretch;
}

/* ===== Brand ===== */
.brand {
  font-family: Arial, sans-serif;
  font-weight: 700;
  font-size: 54px;
  letter-spacing: -1px;
  margin-bottom: 28px;
  align-self: center;
}

.brand--small {
  font-size: 32px;
  margin-bottom: 18px;
}

.brand__bai {
  color: rgb(78, 110, 242);
}

.brand__du {
  background: rgb(78, 110, 242);
  color: #fff;
  border-radius: 8px;
  padding: 0 4px;
  margin: 0 1px;
}

.brand__cn {
  color: rgb(78, 110, 242);
}

/* ===== Search box ===== */
.searchbox {
  width: 100%;
  border: 2px solid rgb(78, 110, 242);
  border-radius: 16px;
  padding: 16px 18px 12px;
  box-shadow: 0 2px 10px rgba(78, 110, 242, 0.08);
  background: #fff;
}

.searchbox__input {
  width: 100%;
  resize: none;
  font-size: 16px;
  line-height: 1.5;
  color: rgb(34, 34, 34);
  background: transparent;
}

.searchbox__input::placeholder {
  color: rgb(145, 149, 163);
}

.searchbox__toolbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 18px;
  margin-top: 8px;
}

.searchbox__icons {
  display: flex;
  align-items: center;
  gap: 18px;
  color: rgb(145, 149, 163);
}

.searchbox__icon {
  font-size: 18px;
  cursor: pointer;
  opacity: 0.7;
}

.searchbox__icon:hover {
  opacity: 1;
}

.searchbox__btn {
  background: linear-gradient(135deg, rgb(78, 110, 242), rgb(110, 96, 240));
  color: #fff;
  font-size: 15px;
  padding: 10px 26px;
  border-radius: 20px;
  transition: opacity 0.2s;
}

.searchbox__btn:hover {
  opacity: 0.9;
}

/* ===== Wenxin banner ===== */
.wenxin {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgb(246, 247, 254);
  border-radius: 22px;
  padding: 10px 18px;
  margin-top: 28px;
  cursor: pointer;
  font-size: 14px;
  color: rgb(51, 51, 51);
}

.wenxin__icon {
  background: rgb(78, 110, 242);
  color: #fff;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
}

.wenxin__arrow {
  color: rgb(145, 149, 163);
}

/* ===== Hot search ===== */
.hot {
  width: 100%;
  margin-top: 44px;
}

.hot__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.hot__title {
  font-size: 18px;
  font-weight: 700;
  color: rgb(34, 34, 34);
}

.hot__title-accent {
  color: rgb(254, 45, 70);
}

.hot__refresh {
  font-size: 13px;
  color: rgb(145, 149, 163);
  cursor: pointer;
}

.hot__list {
  list-style: none;
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 48px;
  row-gap: 4px;
}

.hot__item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 6px;
  border-radius: 8px;
  cursor: pointer;
}

.hot__item:hover {
  background: rgb(246, 247, 254);
}

.hot__rank {
  font-size: 15px;
  font-weight: 700;
  width: 16px;
  text-align: center;
}

.hot__rank--top {
  color: rgb(254, 45, 70);
}

.hot__rank--normal {
  color: rgb(187, 187, 187);
}

.hot__label {
  font-size: 14px;
  color: rgb(34, 34, 34);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hot__item:hover .hot__label {
  color: rgb(78, 110, 242);
}

.hot__tag {
  font-size: 11px;
  color: #fff;
  padding: 1px 5px;
  border-radius: 3px;
}

.hot__tag--hot {
  background: rgb(255, 69, 91);
}

.hot__tag--new {
  background: rgb(255, 69, 91);
}

.hot__tag--rec {
  background: rgb(255, 102, 0);
}

/* ===== Results ===== */
.results {
  width: 100%;
  margin-top: 24px;
}

.results__meta {
  font-size: 13px;
  color: rgb(145, 149, 163);
  margin-bottom: 18px;
}

.results__meta strong {
  color: rgb(78, 110, 242);
}

.results__list {
  list-style: none;
}

.result {
  margin-bottom: 24px;
}

.result__title {
  font-size: 18px;
  color: rgb(0, 0, 238);
  line-height: 1.4;
}

.result__title:hover {
  text-decoration: underline;
}

.result__url {
  font-size: 13px;
  color: rgb(0, 128, 0);
  margin: 4px 0;
  word-break: break-all;
}

.result__summary {
  font-size: 14px;
  color: rgb(51, 51, 51);
  line-height: 1.6;
}

/* ===== Pagination ===== */
.pagination {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 32px 0 48px;
}

.pagination__btn {
  font-size: 14px;
  color: rgb(78, 110, 242);
  border: 1px solid rgb(78, 110, 242);
  padding: 8px 18px;
  border-radius: 6px;
  background: #fff;
  transition: background 0.2s, color 0.2s;
}

.pagination__btn:hover:not(:disabled) {
  background: rgb(78, 110, 242);
  color: #fff;
}

.pagination__btn:disabled {
  color: rgb(187, 187, 187);
  border-color: rgb(221, 221, 221);
  cursor: not-allowed;
}

.pagination__page {
  font-size: 14px;
  color: rgb(51, 51, 51);
}

/* ===== Footer ===== */
.footer {
  margin-top: auto;
  padding: 18px 16px;
  background: rgb(251, 251, 251);
  text-align: center;
}

.footer__links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 14px;
  font-size: 12px;
  color: rgb(145, 149, 163);
}

.footer__links a:hover {
  color: rgb(78, 110, 242);
}
```