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
