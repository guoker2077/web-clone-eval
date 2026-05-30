import './TopNav.css'

const navItems = [
  '新闻',
  'hao123',
  '地图',
  '贴吧',
  '视频',
  '图片',
  '网盘',
  '文库',
  '文心',
  '搭子DuMate',
  '更多',
]

export default function TopNav() {
  return (
    <nav className="top-nav">
      <div className="top-nav__links">
        {navItems.map((item) => (
          <a key={item} href="#" className="top-nav__link">
            {item}
          </a>
        ))}
      </div>
    </nav>
  )
}
