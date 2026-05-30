import SearchBox from './SearchBox'
import './HomePage.css'

interface Props {
  query: string
  setQuery: (q: string) => void
  onSearch: (q: string) => void
}

const navLinks = ['图片', '视频', '翻译', '地图', '学术', '···']

const heroNews = [
  { title: '诺基亚发布首款微聊手机', color: 'linear-gradient(135deg,#3a4a5a,#6b7b8b)' },
  { title: '九寨沟照镜子被索要2元？', color: 'linear-gradient(135deg,#2f6b4f,#5aa07a)' },
  { title: '比亚迪发布超级智能体迪迪虾', color: 'linear-gradient(135deg,#1a1a1a,#444)' },
  { title: '英伟达黄仁勋评价韬定律', color: 'linear-gradient(135deg,#243b53,#456)' },
  { title: '必应学术搜索火热上新', color: 'linear-gradient(135deg,#0a5a8a,#2b8ccc)' },
]

const cards = [
  { src: '华声在线', time: '2 天', title: '肝不好，头先知！这些头部信号一出现，立即检查别拖延！', color: 'linear-gradient(135deg,#d8c3a5,#b89b7c)' },
  { src: '博禾医生', time: '3 千', title: '一周至少15次!52岁男子肾衰竭，妻子：劝了很多次，就是不听', color: 'linear-gradient(135deg,#e8d5c0,#caa982)' },
  { src: '一点资讯', time: '19 小时', title: '相差六岁，姐弟恋，领证七年生下两个孩子后才举行婚礼', color: 'linear-gradient(135deg,#c0392b,#e57373)' },
  { src: '华声在线', time: '1 天', title: '长肉巨快的5种食物，面条只排第二，第一名很多人没想到', color: 'linear-gradient(135deg,#f0c14b,#e6a817)' },
  { src: '光影新视界', time: '3 天', title: '刘浩存拍完主角后不敢去孙浩家 原来是怕进门先背台词', color: 'linear-gradient(135deg,#5a4a6a,#8a6a9a)' },
  { src: '一点资讯', time: '视频', title: '熊猫团子躲在墙角生闷气，饲养员安慰不料反被打', color: 'linear-gradient(135deg,#4a5a6a,#7a8a9a)' },
  { src: '人民网', time: '7 小时', title: '神舟二十二号载人飞船返回舱成功着陆', color: 'linear-gradient(135deg,#c0392b,#d35400)' },
  { src: 'ZAKER娱乐', time: '1 天', title: '女演员长相有多重要？43岁高露给小14岁李昀锐演妈', color: 'linear-gradient(135deg,#6a8a5a,#9ab87a)' },
  { src: '一点资讯', time: '17 小时', title: '曾因言论翻车今又惹怒跑男粉，白鹿一月掉粉百万', color: 'linear-gradient(135deg,#8a5a6a,#b87a8a)' },
]

export default function HomePage({ query, setQuery, onSearch }: Props) {
  return (
    <div className="home">
      <header className="bing-nav">
        <div className="nav-left">
          <span className="ms-logo">
            <span className="ms-grid">
              <i style={{ background: '#f25022' }} />
              <i style={{ background: '#7fba00' }} />
              <i style={{ background: '#00a4ef' }} />
              <i style={{ background: '#ffb900' }} />
            </span>
            <span className="ms-text">Microsoft Bing</span>
          </span>
          <nav className="nav-links">
            {navLinks.map((l) => (
              <a key={l}>{l}</a>
            ))}
          </nav>
        </div>
        <div className="nav-right">
          <a className="nav-pill">登录 <span className="dot avatar" /></a>
          <a className="nav-pill">Rewards <span className="dot reward" /></a>
          <a className="nav-pill">手机版 <span className="dot phone" /></a>
          <button className="hamburger" aria-label="菜单">≡</button>
        </div>
      </header>

      <section className="hero">
        <svg
          className="mountains"
          viewBox="0 0 1440 620"
          preserveAspectRatio="xMidYMid slice"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#0f2c47" />
              <stop offset="55%" stopColor="#3d7099" />
              <stop offset="100%" stopColor="#7aa9c9" />
            </linearGradient>
            <linearGradient id="peak" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f7c97a" />
              <stop offset="35%" stopColor="#e89a4f" />
              <stop offset="100%" stopColor="#566472" />
            </linearGradient>
          </defs>
          <rect width="1440" height="620" fill="url(#sky)" />
          <polygon
            points="0,620 0,430 250,310 480,410 700,270 920,420 1180,300 1440,440 1440,620"
            fill="#2f4a5e"
            opacity="0.55"
          />
          <polygon points="560,620 980,150 1440,620" fill="url(#peak)" />
          <polygon points="900,300 980,150 1062,300 980,250" fill="#ffffff" opacity="0.85" />
          <polygon
            points="0,620 360,360 720,520 1100,380 1440,560 1440,620"
            fill="#335a6e"
          />
        </svg>

        <div className="search-wrap">
          <SearchBox value={query} onChange={setQuery} onSearch={onSearch} variant="home" />
        </div>

        <div className="hero-news">
          {heroNews.map((n, i) => (
            <article className="hero-card" key={i}>
              <div className="hero-card-img" style={{ background: n.color }} />
              <span className="hero-card-title">{n.title}</span>
            </article>
          ))}
        </div>
      </section>

      <main className="discover">
        <h2 className="discover-title">发现</h2>
        <div className="cards">
          {cards.map((c, i) => (
            <article className="card" key={i}>
              <div className="card-img" style={{ background: c.color }} />
              <div className="card-meta">
                {c.src} · {c.time}
              </div>
              <h3 className="card-title">{c.title}</h3>
            </article>
          ))}
        </div>
      </main>
    </div>
  )
}
