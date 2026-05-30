import { useState } from 'react'
import HomePage from './components/HomePage'
import ResultsPage from './components/ResultsPage'

export default function App() {
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [page, setPage] = useState(1)
  const [view, setView] = useState<'home' | 'results'>('home')

  const handleSearch = (q: string) => {
    const trimmed = q.trim()
    if (!trimmed) return
    setQuery(trimmed)
    setSubmitted(trimmed)
    setPage(1)
    setView('results')
  }

  const goHome = () => {
    setView('home')
  }

  if (view === 'home') {
    return <HomePage query={query} setQuery={setQuery} onSearch={handleSearch} />
  }

  return (
    <ResultsPage
      query={query}
      setQuery={setQuery}
      submitted={submitted}
      page={page}
      setPage={setPage}
      onSearch={handleSearch}
      onHome={goHome}
    />
  )
}
