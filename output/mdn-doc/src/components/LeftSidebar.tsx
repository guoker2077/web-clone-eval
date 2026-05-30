import { useState } from 'react'
import '../styles/sidebar.css'

const elements = [
  '<a>',
  '<abbr>',
  '<acronym>',
  '<address>',
  '<area>',
  '<article>',
  '<aside>',
  '<audio>',
  '<b>',
  '<base>',
  '<bdi>',
  '<bdo>',
]

export default function LeftSidebar() {
  const [filter, setFilter] = useState('')

  const shown = elements.filter((e) =>
    e.toLowerCase().includes(filter.toLowerCase()),
  )

  return (
    <aside className="left-sidebar" aria-label="Related Topics">
      <div className="sidebar-filter">
        <input
          type="text"
          className="filter-input"
          placeholder="Filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          aria-label="Filter sidebar"
        />
        <button type="button" className="add-button">
          + Add JavaScript
        </button>
      </div>

      <nav className="sidebar-nav">
        <h2 className="sidebar-heading">Reference</h2>
        <details open className="sidebar-group">
          <summary>Elements</summary>
          <ul className="sidebar-list">
            {shown.map((el) => (
              <li key={el}>
                <a
                  className={el === '<a>' ? 'sidebar-link active' : 'sidebar-link'}
                  href={`/en-US/docs/Web/HTML/Reference/Elements/${el.replace(/[<>]/g, '')}`}
                >
                  {el}
                </a>
              </li>
            ))}
          </ul>
        </details>
      </nav>
    </aside>
  )
}
