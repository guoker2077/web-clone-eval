import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <nav className="footer__nav" aria-label="Footer">
        <a href="https://docs.github.com/site-policy/github-terms/github-terms-of-service">
          Terms
        </a>
        <a href="https://docs.github.com/site-policy/privacy-policies/github-privacy-statement">
          Privacy
        </a>
        <a href="https://docs.github.com">Docs</a>
        <a href="https://support.github.com">Contact GitHub Support</a>
        <button type="button" className="footer__link-btn">
          Manage cookies
        </button>
        <button type="button" className="footer__link-btn">
          Do not share my personal information
        </button>
      </nav>
    </footer>
  )
}

export default Footer
