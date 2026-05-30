import type { ChangeEvent, FormEvent } from 'react'
import './SearchBox.css'

interface Props {
  value: string
  onChange: (v: string) => void
  onSearch: (v: string) => void
  variant?: 'home' | 'results'
}

export default function SearchBox({ value, onChange, onSearch, variant = 'home' }: Props) {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onSearch(value)
  }

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value)
  }

  return (
    <form
      className={`sb_form sb_${variant}`}
      onSubmit={handleSubmit}
      role="search"
      action="#"
    >
      <input
        id="sb_form_q"
        name="q"
        data-testid="search-input"
        className="sb_input"
        type="text"
        value={value}
        onChange={handleChange}
        autoComplete="off"
        aria-label="搜索"
        placeholder=""
      />

      <span className="sb_mic" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="18" height="18">
          <path
            fill="currentColor"
            d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V22h2v-3.08A7 7 0 0 0 19 12h-2z"
          />
        </svg>
      </span>

      <button
        id="sb_form_go"
        data-testid="search-button"
        className="sb_go"
        type="submit"
        aria-label="搜索"
      >
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path
            fill="currentColor"
            d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 1 0-.7.7l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0A4.5 4.5 0 1 1 14 9.5 4.49 4.49 0 0 1 9.5 14z"
          />
        </svg>
      </button>
    </form>
  )
}
