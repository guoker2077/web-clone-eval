===FILE: package.json===
{
  "name": "baidu-clone",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
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
    "noUnusedLocals": true,
    "noUnusedParameters": true,
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
    "strict": true
  },
  "include": ["vite.config.ts"]
}

===FILE: index.html===
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

===FILE: public/favicon.svg===
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#4e6ef2"/>
  <text x="16" y="22" font-size="18" text-anchor="middle" fill="#fff" font-family="Arial">百</text>
</svg>

===FILE: src/main.tsx===
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

===FILE: src/index.css===
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
  background: rgb(255, 255, 255);
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
  background: transparent;
}

===FILE: src/data.ts===
export interface SearchResult {
  title: string
  summary: string
  source: string
  url: string
}

const summaryTemplates = [
  '关于「{kw}」的最新资讯与深度解读，涵盖背景介绍、核心要点以及网友热议话题，帮助你快速了解全貌。',
  '{kw} 是近期备受关注的话题。本文从多个角度梳理了相关信息，包括定义、发展历程以及实际应用场景。',
  '想了解 {kw} 吗？这里汇总了权威来源的内容，提供详细说明与实用建议，让你一文读懂。',
  '最新「{kw}」相关报道：业内专家给出分析，结合数据与案例，解析其中的关键问题与未来趋势。',
  '{kw} 全面解析。包含常见问题解答、操作指南以及相关推荐，适合初学者和进阶用户参考阅读。',
  '围绕 {kw} 的讨论持续升温，本页整理了网络上的主流观点与最新动态，内容客观全面。',
  '{kw} 百科：基础概念、相关知识点和延伸阅读一应俱全，是了解该主题的良好起点。',
  '关于 {kw} 的实用攻略，手把手教你从入门到熟练，附带图文说明与注意事项。',
]

const sources = [
  '百度百科',
  '百家号',
  '知乎',
  '人民网',
  '新华网',
  '中国新闻网',
  '百度知道',
  '搜狐',
]

const titleSuffixes = [
  '_百度百科',
  ' - 最新消息汇总',
  '：你需要知道的一切',
  ' 详细解读与分析',
  ' 全面介绍',
  '相关内容推荐',
  ' 最新进展',
  '是什么？一文读懂',
]

export function generateResults(keyword: string, page: number, pageSize = 8): SearchResult[] {
  const kw = keyword.trim() || '百度'
  const results: SearchResult[] = []
  for (let i = 0; i < pageSize; i++) {
    const index = (page - 1) * pageSize + i
    results.push({
      title: `${kw}${titleSuffixes[index % titleSuffixes.length]}`,
      summary: summaryTemplates[index % summaryTemplates.length].replace(/\{kw\}/g, kw),
      source: sources[index % sources.length],
      url: `https://www.baidu.com/s?wd=${encodeURIComponent(kw)}&pn=${index}`,
    })
  }
  return results
}

export const navLinks = ['新闻', 'hao123', '地图', '贴吧', '视频', '图片', '网盘', '学术', '更多DuMate', '设置']

export const hotList = [
  '中央气象台发布暴雨黄色预警',
  '专家称应警惕“假理财”',
  '14岁少年勇救落水者 获表彰',
  '多地迎来降温 注意添衣保暖',
  '“低空经济” 释放新动能',
  '新能源汽车销量再创新高',
  '人工智能助力医疗诊断 提升效率',
  '高校毕业生超200万 就业季来临',
  '消费市场持续回暖 信心增强',
  '城市更新行动加速推进',
]

===FILE: src/App.tsx===
import { useState } from 'react'
import { generateResults, navLinks, hotList } from './data'
import type { SearchResult } from './data'
import './App.css'

export default function App() {
  const [query, setQuery] = useState('')
  const [searched, setSearched] = useState(false)
  const [submittedKeyword, setSubmittedKeyword] = useState('')
  const [page, setPage] = useState(1)
  const [results, setResults] = useState<SearchResult[]>([])

  const runSearch = (keyword: string, pageNum: number) => {
    const kw = keyword.trim()
    if (!kw) return
    const data = generateResults(kw, pageNum)
    setResults(data)
    setSubmittedKeyword(kw)
    setPage(pageNum)
    setSearched(true)
  }

  const handleSearch = () => {
    runSearch(query, 1)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const handlePrev = () => {
    if (page > 1) {
      runSearch(submittedKeyword, page - 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const handleNext = () => {
    runSearch(submittedKeyword, page + 1)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const goHome = () => {
    setSearched(false)
    setResults([])
    setSubmittedKeyword('')
    setPage(1)
  }

  return (
    <div className="app">
      <header className="topnav">
        <div className="topnav-links">
          {navLinks.map((link) => (
            <a key={link} href="#" className="topnav-link" onClick={(e) => e.preventDefault()}>
              {link}
            </a>
          ))}
        </div>
        <div className="topnav-right">
          <a href="#" className="topnav-link" onClick={(e) => e.preventDefault()}>
            登录
          </a>
        </div>
      </header>

      {!searched ? (
        <main className="home">
          <div className="logo" onClick={goHome}>
            <span className="logo-bai">Bai</span>
            <span className="logo-du">du</span>
            <span className="logo-cn">百度</span>
          </div>

          <div className="search-box">
            <textarea
              className="search-input"
              data-testid="search-input"
              placeholder="百度一下，你就知道，开启AI搜索新体验"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
            />
            <div className="search-tools">
              <div className="search-icons">
                <span className="tool-icon" title="语音">🎤</span>
                <span className="tool-icon" title="附件">📎</span>
                <span className="tool-icon" title="图片">🖼️</span>
              </div>
              <button
                className="search-button"
                data-testid="search-button"
                onClick={handleSearch}
              >
                百度一下
              </button>
            </div>
          </div>

          <div className="wenxin-banner">
            <span className="wenxin-icon">文心</span>
            <span className="wenxin-text">文心大模型，与你一起开启智能创作之旅</span>
            <span className="wenxin-arrow">›</span>
          </div>

          <section className="hot-section">
            <div className="hot-header">
              <div className="hot-title">
                百度热<span className="hot-title-accent">搜</span> ›
              </div>
              <div className="hot-refresh">↻ 换一换</div>
            </div>
            <div className="hot-grid">
              {hotList.map((item, i) => (
                <div
                  className="hot-item"
                  key={item}
                  onClick={() => {
                    setQuery(item)
                    runSearch(item, 1)
                  }}
                >
                  <span className={`hot-rank rank-${i + 1}`}>{i + 1}</span>
                  <span className="hot-text">{item}</span>
                </div>
              ))}
            </div>
          </section>
        </main>
      ) : (
        <main className="results-page">
          <div className="results-search-bar">
            <div className="logo small" onClick={goHome}>
              <span className="logo-bai">Bai</span>
              <span className="logo-du">du</span>
              <span className="logo-cn">百度</span>
            </div>
            <div className="results-search-box">
              <textarea
                className="search-input results"
                data-testid="search-input"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={1}
              />
              <button
                className="search-button"
                data-testid="search-button"
                onClick={handleSearch}
              >
                百度一下
              </button>
            </div>
          </div>

          <div className="results-meta">
            搜索 <strong>{submittedKeyword}</strong> 找到约 1,230,000 条相关结果（第 {page} 页）
          </div>

          <div className="result-list" data-testid="result-list">
            {results.map((r, i) => (
              <div className="result-item" key={`${page}-${i}`}>
                <a
                  className="result-title"
                  href={r.url}
                  onClick={(e) => e.preventDefault()}
                >
                  {r.title}
                </a>
                <div className="result-summary">{r.summary}</div>
                <div className="result-source">{r.source}</div>
              </div>
            ))}
          </div>

          <div className="pagination" data-testid="pagination">
            <button
              className="page-btn"
              data-testid="prev-page"
              onClick={handlePrev}
              disabled={page <= 1}
            >
              上一页
            </button>
            <span className="page-current">第 {page} 页</span>
            <button className="page-btn next" data-testid="next-page" onClick={handleNext}>
              下一页 ›
            </button>
          </div>
        </main>
      )}

      <footer className="footer">
        <div className="footer-links">
          <a href="#" onClick={(e) => e.preventDefault()}>
            关于百度
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            About Baidu
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            使用百度前必读
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            意见反馈
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            帮助中心
          </a>
        </div>
        <div className="footer-copy">
          京公网安备11000002000001号 京ICP证030173号 © Baidu 使用前必读
        </div>
      </footer>
    </div>
  )
}

===FILE: src/App.css===
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Top nav */
.topnav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 24px;
}

.topnav-links {
  display: flex;
  align-items: center;
  gap: 22px;
}

.topnav-link {
  font-size: 13px;
  color: rgb(34, 34, 34);
}

.topnav-link:hover {
  color: rgb(78, 110, 242);
}

.topnav-right .topnav-link {
  color: rgb(78, 110, 242);
}

/* Logo */
.logo {
  font-size: 52px;
  font-weight: 700;
  font-family: Arial, sans-serif;
  letter-spacing: -1px;
  cursor: pointer;
  user-select: none;
}

.logo .logo-bai {
  color: rgb(78, 110, 242);
}
.logo .logo-du {
  color: rgb(254, 45, 70);
}
.logo .logo-cn {
  color: rgb(78, 110, 242);
}

.logo.small {
  font-size: 30px;
  flex-shrink: 0;
}

/* Home */
.home {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
}

.home .logo {
  margin-bottom: 30px;
}

/* Search box */
.search-box {
  width: 800px;
  max-width: 90%;
  border: 2px solid rgb(78, 110, 242);
  border-radius: 14px;
  padding: 16px 18px 12px;
  box-shadow: 0 4px 16px rgba(78, 110, 242, 0.08);
}

.search-input {
  width: 100%;
  font-size: 16px;
  color: rgb(34, 34, 34);
  resize: none;
  line-height: 1.5;
  min-height: 28px;
  overflow: hidden;
}

.search-input::placeholder {
  color: rgb(145, 149, 163);
}

.search-tools {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  margin-top: 18px;
}

.search-icons {
  display: flex;
  gap: 18px;
  align-items: center;
}

.tool-icon {
  font-size: 18px;
  cursor: pointer;
  opacity: 0.7;
}

.tool-icon:hover {
  opacity: 1;
}

.search-button {
  background: linear-gradient(135deg, rgb(78, 110, 242), rgb(108, 138, 255));
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 10px 26px;
  font-size: 15px;
  font-weight: 500;
}

.search-button:hover {
  background: linear-gradient(135deg, rgb(64, 96, 230), rgb(94, 124, 245));
}

/* Wenxin banner */
.wenxin-banner {
  margin-top: 30px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgb(246, 247, 254);
  border-radius: 20px;
  padding: 8px 18px;
  font-size: 14px;
  color: rgb(51, 51, 51);
  cursor: pointer;
}

.wenxin-icon {
  background: rgb(78, 110, 242);
  color: #fff;
  font-size: 12px;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wenxin-arrow {
  color: rgb(145, 149, 163);
}

/* Hot section */
.hot-section {
  width: 800px;
  max-width: 90%;
  margin-top: 50px;
}

.hot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.hot-title {
  font-size: 18px;
  font-weight: 700;
  color: rgb(34, 34, 34);
}

.hot-title-accent {
  color: rgb(78, 110, 242);
}

.hot-refresh {
  font-size: 13px;
  color: rgb(145, 149, 163);
  cursor: pointer;
}

.hot-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 60px;
  row-gap: 14px;
}

.hot-item {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-size: 15px;
}

.hot-item:hover .hot-text {
  color: rgb(78, 110, 242);
}

.hot-rank {
  width: 18px;
  text-align: center;
  font-size: 14px;
  font-style: italic;
  color: rgb(187, 187, 187);
  flex-shrink: 0;
}

.hot-rank.rank-1 {
  color: rgb(254, 45, 70);
}
.hot-rank.rank-2 {
  color: rgb(255, 102, 0);
}
.hot-rank.rank-3 {
  color: rgb(255, 170, 0);
}

.hot-text {
  color: rgb(34, 34, 34);
}

/* Results page */
.results-page {
  flex: 1;
  padding: 0 0 40px;
}

.results-search-bar {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 16px 40px;
  border-bottom: 1px solid #eee;
}

.results-search-box {
  display: flex;
  align-items: center;
  flex: 1;
  max-width: 640px;
  border: 2px solid rgb(78, 110, 242);
  border-radius: 12px;
  padding: 6px 6px 6px 16px;
}

.search-input.results {
  flex: 1;
  min-height: 24px;
  font-size: 15px;
}

.results-search-box .search-button {
  padding: 8px 22px;
  border-radius: 8px;
}

.results-meta {
  padding: 16px 40px 8px;
  font-size: 13px;
  color: rgb(145, 149, 163);
}

.results-meta strong {
  color: rgb(78, 110, 242);
}

.result-list {
  padding: 0 40px;
  max-width: 720px;
}

.result-item {
  padding: 16px 0;
  border-bottom: 1px solid #f3f3f3;
}

.result-title {
  font-size: 18px;
  color: rgb(0, 0, 238);
  line-height: 1.4;
}

.result-title:hover {
  text-decoration: underline;
}

.result-summary {
  margin-top: 8px;
  font-size: 14px;
  color: rgb(51, 51, 51);
  line-height: 1.6;
}

.result-source {
  margin-top: 8px;
  font-size: 13px;
  color: rgb(145, 149, 163);
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 40px;
}

.page-btn {
  background: #fff;
  border: 1px solid rgb(78, 110, 242);
  color: rgb(78, 110, 242);
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 14px;
}

.page-btn:hover:not(:disabled) {
  background: rgb(246, 247, 254);
}

.page-btn:disabled {
  border-color: rgb(187, 187, 187);
  color: rgb(187, 187, 187);
  cursor: not-allowed;
}

.page-btn.next {
  background: rgb(78, 110, 242);
  color: #fff;
}

.page-btn.next:hover {
  background: rgb(64, 96, 230);
}

.page-current {
  font-size: 14px;
  color: rgb(51, 51, 51);
}

/* Footer */
.footer {
  background: rgb(251, 251, 251);
  padding: 18px 40px;
  text-align: center;
  font-size: 12px;
  color: rgb(145, 149, 163);
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 18px;
  margin-bottom: 8px;
}

.footer-links a:hover {
  color: rgb(78, 110, 242);
}

.footer-copy {
  color: rgb(187, 187, 187);
}