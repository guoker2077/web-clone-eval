function Footer() {
  const links = [
    { label: 'Terms', href: '#' },
    { label: 'Privacy', href: '#' },
    { label: 'Docs', href: '#' },
    { label: 'Contact GitHub Support', href: '#' },
    { label: 'Manage cookies', href: '#' },
    { label: 'Do not share my personal information', href: '#' },
  ]

  return (
    <footer className="site-footer">
      <ul className="footer-links">
        {links.map((link) => (
          <li key={link.label}>
            <a href={link.href} onClick={(e) => e.preventDefault()}>
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </footer>
  )
}

export default Footer
