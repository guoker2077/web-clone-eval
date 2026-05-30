import { hotList } from '../data/mock'
import './HotSearch.css'

interface HotSearchProps {
  onItemClick: (text: string) => void
}

export default function HotSearch({ onItemClick }: HotSearchProps) {
  return (
    <section className="hot-search">
      <div className="hot-search__head">
        <span className="hot-search__title">
          百度<span className="hot-search__title-accent">热搜</span>
          <span className="hot-search__arrow">›</span>
        </span>
        <button className="hot-search__refresh" type="button">
          <RefreshIcon /> 换一换
        </button>
      </div>
      <ul className="hot-search__list">
        {hotList.map((item, index) => (
          <li key={item.id} className="hot-search__item">
            <button
              className="hot-search__entry"
              type="button"
              onClick={() => onItemClick(item.text)}
            >
              <span className={`hot-search__rank rank-${index + 1}`}>
                {index + 1}
              </span>
              <span className="hot-search__text">{item.text}</span>
              {item.tag && (
                <span className={`hot-search__tag tag--${item.tag}`}>
                  {item.tag === 'hot' ? '热' : '新'}
                </span>
              )}
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}

function RefreshIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 12a9 9 0 1 1-2.64-6.36" />
      <path d="M21 3v6h-6" />
    </svg>
  )
}
