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
