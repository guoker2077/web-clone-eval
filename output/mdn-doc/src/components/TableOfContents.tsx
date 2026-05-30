import '../styles/toc.css'

const items = [
  { id: 'try_it', label: 'Try it', testid: 'toc-try-it' },
  { id: 'attributes', label: 'Attributes', testid: 'toc-attributes' },
  { id: 'accessibility', label: 'Accessibility', testid: 'toc-accessibility' },
  { id: 'examples', label: 'Examples', testid: 'toc-examples' },
  {
    id: 'security_and_privacy',
    label: 'Security and privacy',
    testid: 'toc-security-privacy',
  },
  {
    id: 'technical_summary',
    label: 'Technical summary',
    testid: 'toc-technical-summary',
  },
  { id: 'specifications', label: 'Specifications', testid: 'toc-specifications' },
  {
    id: 'browser_compatibility',
    label: 'Browser compatibility',
    testid: 'toc-browser-compatibility',
  },
  { id: 'see_also', label: 'See also', testid: 'toc-see-also' },
]

export default function TableOfContents() {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault()
    const target = document.getElementById(id)
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      history.replaceState(null, '', `#${id}`)
    }
  }

  return (
    <aside className="toc" aria-label="In this article">
      <div className="toc-sticky">
        <h2 className="toc-title">In this article</h2>
        <ul className="toc-list" data-testid="toc-list">
          {items.map((item) => (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                data-testid={item.testid}
                onClick={(e) => handleClick(e, item.id)}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  )
}
