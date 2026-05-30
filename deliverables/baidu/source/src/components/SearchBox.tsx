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
