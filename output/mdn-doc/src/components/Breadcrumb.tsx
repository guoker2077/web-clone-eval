import '../styles/breadcrumb.css'

export default function Breadcrumb() {
  return (
    <nav className="breadcrumb" aria-label="Breadcrumb">
      <ol className="breadcrumb-list">
        <li>
          <a href="/en-US/docs/Web" data-testid="breadcrumb-web">
            Web
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a href="/en-US/docs/Web/HTML" data-testid="breadcrumb-html">
            HTML
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a href="/en-US/docs/Web/HTML/Reference" data-testid="breadcrumb-reference">
            Reference
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a
            href="/en-US/docs/Web/HTML/Reference/Elements"
            data-testid="breadcrumb-elements"
          >
            Elements
          </a>
          <span className="sep">/</span>
        </li>
        <li>
          <a
            className="current"
            aria-current="page"
            href="/en-US/docs/Web/HTML/Reference/Elements/a"
            data-testid="breadcrumb-anchor"
          >
            &lt;a&gt;
          </a>
        </li>
      </ol>
    </nav>
  )
}
