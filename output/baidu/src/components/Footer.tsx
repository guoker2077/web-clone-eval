import './Footer.css'

const links = [
  '关于百度',
  'About Baidu',
  '使用百度前必读',
  '帮助中心',
  '企业推广',
]

const records = [
  '京公网安备11000002000001号',
  '京ICP证030173号',
  '互联网新闻信息服务许可11220180008',
  '网络文化经营许可证：京网文〔2026〕0171-042号',
]

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer__links">
        {links.map((link) => (
          <a key={link} href="#" className="footer__link">
            {link}
          </a>
        ))}
      </div>
      <div className="footer__records">
        {records.map((rec) => (
          <span key={rec} className="footer__record">
            {rec}
          </span>
        ))}
      </div>
    </footer>
  )
}
