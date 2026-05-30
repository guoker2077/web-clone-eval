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
