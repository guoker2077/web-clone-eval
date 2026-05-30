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
