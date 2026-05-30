===FILE: package.json===
{
  "name": "bing-search-clone",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.1.0"
  }
}

===FILE: vite.config.ts===
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})

===FILE: tsconfig.json===
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}

===FILE: tsconfig.node.json===
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}

===FILE: index.html===
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Microsoft Bing 搜索</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>

===FILE: src/main.tsx===
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
)

===FILE: src/index.css===
* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
}

body {
  font-family: "Segoe UI", Segoe, Tahoma, Arial, Verdana, sans-serif;
  color: rgb(17, 17, 17);
  background: #ffffff;
  -webkit-font-smoothing: antialiased;
}

#root {
  min-height: 100vh;
}

a {
  color: inherit;
}

button {
  font-family: inherit;
}

===FILE: src/App.tsx===
import { useState } from 'react'
import TopNav from './components/TopNav'
import Hero from './components/Hero'
import DiscoverFeed from './components/DiscoverFeed'
import SearchResultsPage from './components/SearchResultsPage'
import './App.css'

export default function App() {
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [page, setPage] = useState(1)
  const [searched, setSearched] = useState(false)

  const handleSearch = (q: string) => {
    const term = q.trim()
    if (!term) return
    setQuery(term)
    setSubmitted(term)
    setPage(1)
    setSearched(true)
  }

  const handleHome = () => {
    setSearched(false)
    setQuery('')
    setSubmitted('')
    setPage(1)
  }

  if (searched) {
    return (
      <SearchResultsPage
        query={query}
        setQuery={setQuery}
        submitted={submitted}
        page={page}
        onSearch={handleSearch}
        onNextPage={() => setPage((p) => p + 1)}
        onPrevPage={() => setPage((p) => Math.max(1, p - 1))}
        onGoToPage={(p) => setPage(p)}
        onHome={handleHome}
      />
    )
  }

  return (
    <div className="app-home">
      <TopNav />
      <Hero query={query} setQuery={setQuery} onSearch={handleSearch} />
      <DiscoverFeed />
    </div>
  )
}

===FILE: src/App.css===
.app-home {
  min-height: 100vh;
  background: rgb(236, 236, 236);
}

===FILE: src/data/mockResults.ts===
export interface SearchResult {
  title: string
  displayUrl: string
  snippet: string
}

interface Source {
  name: string
  host: string
}

const sources: Source[] = [
  { name: '百度百科', host: 'baike.baidu.com' },
  { name: '维基百科', host: 'zh.wikipedia.org' },
  { name: '知乎', host: 'www.zhihu.com' },
  { name: '微博', host: 'weibo.com' },
  { name: '人民网', host: 'www.people.com.cn' },
  { name: '新华网', host: 'www.xinhuanet.com' },
  { name: '哔哩哔哩', host: 'www.bilibili.com' },
  { name: 'CSDN', host: 'blog.csdn.net' },
]

const perPage = 9

export function generateResults(query: string, page: number): SearchResult[] {
  const q = query && query.trim() ? query.trim() : '搜索'
  const start = (page - 1) * perPage
  const arr: SearchResult[] = []

  for (let i = 0; i < perPage; i++) {
    const idx = start + i + 1
    const src = sources[idx % sources.length]
    arr.push({
      title: `${q} - ${src.name}（第 ${idx} 条相关结果）`,
      displayUrl: `https://www.${src.host}/s?q=${encodeURIComponent(q)}&p=${page}`,
      snippet:
        `这是关于“${q}”的网页摘要。${src.name} 收录了与“${q}”相关的丰富内容，` +
        `包含定义、详细说明、最新资讯与网友讨论，帮助你快速、全面地了解“${q}”的方方面面。`,
    })
  }

  return arr
}

export function totalResultCount(query: string): number {
  const q = query && query.trim() ? query.trim() : '搜索'
  let hash = 0
  for (let i = 0; i < q.length; i++) {
    hash = (hash * 31 + q.charCodeAt(i)) % 9000000
  }
  return 1200000 + hash
}

===FILE: src/components/icons.tsx===
export function MicIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M12 14a3 3 0 0 0 3-3V6a3 3 0 1 0-6 0v5a3 3 0 0 0 3 3Z"
        fill="#737373"
      />
      <path
        d="M18 11a6 6 0 0 1-12 0M12 17v4M8 21h8"
        stroke="#737373"
        strokeWidth="1.6"
        strokeLinecap="round"
        fill="none"
      />
    </svg>
  )
}

export function SearchIcon({ color = '#ffffff' }: { color?: string }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="11" cy="11" r="7" stroke={color} strokeWidth="2" fill="none" />
      <path d="m20 20-3.5-3.5" stroke={color} strokeWidth="2" strokeLinecap="round" />
    </svg>
  )
}

export function MicrosoftLogo() {
  return (
    <svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true">
      <rect x="0" y="0" width="10" height="10" fill="#f25022" />
      <rect x="12" y="0" width="10" height="10" fill="#7fba00" />
      <rect x="0" y="12" width="10" height="10" fill="#00a4ef" />
      <rect x="12" y="12" width="10" height="10" fill="#ffb900" />
    </svg>
  )
}

===FILE: src/components/SearchBar.tsx===
import type { FormEvent } from 'react'
import { MicIcon, SearchIcon } from './icons'
import './SearchBar.css'

interface SearchBarProps {
  query: string
  setQuery: (v: string) => void
  onSearch: (q: string) => void
  variant?: 'hero' | 'compact'
}

export default function SearchBar({
  query,
  setQuery,
  onSearch,
  variant = 'hero',
}: SearchBarProps) {
  const submit = (e: FormEvent) => {
    e.preventDefault()
    onSearch(query)
  }

  return (
    <form className={`search-box ${variant}`} onSubmit={submit} role="search">
      <input
        data-testid="search-input"
        id="sb_form_q"
        name="q"
        className="search-input"
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="搜索网页"
        autoComplete="off"
        aria-label="搜索"
      />
      <button type="button" className="icon-btn mic" aria-label="语音搜索">
        <MicIcon />
      </button>
      <span className="divider" />
      <button
        type="submit"
        data-testid="search-button"
        id="sb_form_go"
        className="icon-btn go"
        aria-label="搜索"
      >
        <SearchIcon color={variant === 'compact' ? '#ffffff' : '#ffffff'} />
      </button>
    </form>
  )
}

===FILE: src/components/SearchBar.css===
.search-box {
  display: flex;
  align-items: center;
  background: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.22);
}

.search-box.hero {
  width: 560px;
  max-width: 92%;
  height: 48px;
  border-radius: 24px;
  padding: 0 6px 0 20px;
}

.search-box.compact {
  width: 480px;
  max-width: 100%;
  height: 44px;
  border-radius: 22px;
  padding: 0 6px 0 18px;
  box-shadow: none;
  border: 1px solid rgb(221, 221, 221);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 16px;
  color: rgb(17, 17, 17);
  height: 100%;
}

.search-input::placeholder {
  color: #9a9a9a;
}

.search-box .icon-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  padding: 0;
}

.search-box .icon-btn.mic:hover {
  background: #f1f1f1;
}

.search-box .divider {
  width: 1px;
  height: 24px;
  background: rgb(221, 221, 221);
  margin: 0 4px;
}

.search-box .icon-btn.go {
  background: #0f6cbd;
}

.search-box .icon-btn.go:hover {
  background: #0c5ba3;
}

.search-box.hero .icon-btn.go {
  width: 40px;
  height: 40px;
}

===FILE: src/components/TopNav.tsx===
import { MicrosoftLogo } from './icons'
import './TopNav.css'

const links = ['图片', '视频', '翻译', '地图', '学术', '•••']

export default function TopNav() {
  return (
    <header className="top-nav">
      <div className="logo">
        <MicrosoftLogo />
        <span className="logo-text">Microsoft Bing</span>
      </div>
      <nav className="nav-links">
        {links.map((l) => (
          <a key={l} href="#" onClick={(e) => e.preventDefault()}>
            {l}
          </a>
        ))}
      </nav>
      <div className="nav-right">
        <a href="#" onClick={(e) => e.preventDefault()} className="nav-pill">
          登录
        </a>
        <a href="#" onClick={(e) => e.preventDefault()} className="nav-pill">
          Rewards
        </a>
        <a href="#" onClick={(e) => e.preventDefault()} className="nav-pill">
          手机版
        </a>
        <button className="hamburger" aria-label="菜单">
          <span />
          <span />
          <span />
        </button>
      </div>
    </header>
  )
}

===FILE: src/components/TopNav.css===
.top-nav {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 26px;
  z-index: 6;
  color: #ffffff;
  font-size: 14px;
}

.top-nav .logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.top-nav .logo-text {
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 22px;
  margin-left: 40px;
}

.nav-links a {
  color: #ffffff;
  text-decoration: none;
  font-size: 15px;
  opacity: 0.95;
}

.nav-links a:hover {
  text-decoration: underline;
}

.nav-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 22px;
}

.nav-right .nav-pill {
  color: #ffffff;
  text-decoration: none;
  font-size: 14px;
  opacity: 0.95;
}

.nav-right .nav-pill:hover {
  text-decoration: underline;
}

.hamburger {
  background: transparent;
  border: none;
  cursor: pointer;
  width: 26px;
  height: 26px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  padding: 0;
}

.hamburger span {
  display: block;
  height: 2px;
  width: 20px;
  background: #ffffff;
  border-radius: 2px;
}

===FILE: src/components/Hero.tsx===
import SearchBar from './SearchBar'
import './Hero.css'

interface HeroProps {
  query: string
  setQuery: (v: string) => void
  onSearch: (q: string) => void
}

export default function Hero({ query, setQuery, onSearch }: HeroProps) {
  return (
    <section className="hero">
      <svg
        className="hero-bg"
        viewBox="0 0 1280 650"
        preserveAspectRatio="xMidYMid slice"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#12305a" />
            <stop offset="45%" stopColor="#3f72ab" />
            <stop offset="100%" stopColor="#88aed3" />
          </linearGradient>
          <linearGradient id="snow" x1="0" y1="0" x2="1" y2="0.5">
            <stop offset="0%" stopColor="#e1eaf3" />
            <stop offset="55%" stopColor="#f3cd86" />
            <stop offset="100%" stopColor="#e89a39" />
          </linearGradient>
        </defs>
        <rect width="1280" height="650" fill="url(#sky)" />
        <polygon
          points="0,470 260,300 520,440 760,320 1040,470 1280,360 1280,650 0,650"
          fill="#26527c"
        />
        <polygon points="380,470 720,150 1080,470" fill="url(#snow)" />
        <polygon
          points="600,300 720,150 840,300 760,360 680,330"
          fill="#f7e6c6"
          opacity="0.85"
        />
        <polygon
          points="0,560 360,400 640,540 920,420 1280,560 1280,650 0,650"
          fill="#15324c"
        />
      </svg>

      <div className="hero-content">
        <SearchBar query={query} setQuery={setQuery} onSearch={onSearch} variant="hero" />
      </div>

      <div className="hero-strip">
        {[
          { t: '诺基亚发布首款微聊手机', c: '#2b2b2b' },
          { t: '九寨沟照镜子被索要2元？', c: '#3c5a73' },
          { t: '比亚迪发布超级智能体迪迪虾', c: '#1a1a2e' },
          { t: '英伟达黄仁勋评价韬定律', c: '#4a4a4a' },
          { t: '必应学术搜索火热上新', c: '#0a6e6e' },
          { t: '电车是时候交养路费了？', c: '#555555' },
        ].map((s) => (
          <div className="strip-card" key={s.t} style={{ background: s.c }}>
            <span>{s.t}</span>
          </div>
        ))}
      </div>
    </section>
  )
}

===FILE: src/components/Hero.css===
.hero {
  position: relative;
  height: 620px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}

.hero-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-content .search-box {
  margin-top: 138px;
}

.hero-strip {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 3;
  display: flex;
  gap: 2px;
  padding: 0;
  height: 130px;
}

.strip-card {
  flex: 1;
  position: relative;
  display: flex;
  align-items: flex-start;
  padding: 12px 14px;
  color: rgba(255, 255, 255, 0.92);
  font-size: 13px;
  line-height: 1.4;
  overflow: hidden;
}

.strip-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.45));
  z-index: 0;
}

.strip-card span {
  position: relative;
  z-index: 1;
}

===FILE: src/components/DiscoverFeed.tsx===
import './DiscoverFeed.css'

interface Card {
  title: string
  source: string
  time: string
  grad: string
  tall?: boolean
}

const cards: Card[] = [
  {
    title: '肝不好，头先知！这些头部信号一出现，立即检查别拖延',
    source: '华声在线',
    time: '2 天',
    grad: 'linear-gradient(135deg,#e8c9a8,#c79b76)',
    tall: true,
  },
  {
    title: '一周至少15次!52岁男子肾衰竭，妻子：劝了很多次，就是不听',
    source: '博禾医生',
    time: '1 天',
    grad: 'linear-gradient(135deg,#d9b3a3,#b88a78)',
  },
  {
    title: '相差六岁，姐弟恋，领证七年生下两个孩子后才举行婚礼',
    source: '一点资讯',
    time: '19 小时',
    grad: 'linear-gradient(135deg,#b33a3a,#7a2727)',
  },
  {
    title: '长肉巨快的5种食物，面条只排第二，第一名很多人没想到',
    source: '华声在线',
    time: '1 天',
    grad: 'linear-gradient(135deg,#e3c07a,#c79b3a)',
  },
  {
    title: '刘浩存拍完主角后不敢去孙浩家 原来是怕进门先背台词',
    source: '光影新视界',
    time: '3 天',
    grad: 'linear-gradient(135deg,#3a2a3a,#1a1020)',
    tall: true,
  },
  {
    title: '熊猫团子躲在墙角生闷气，饲养员安慰不料反被打，下一秒憋住别笑',
    source: '一点资讯·视频',
    time: '视频',
    grad: 'linear-gradient(135deg,#8aa0aa,#5a6e78)',
    tall: true,
  },
  {
    title: '神舟二十二号载人飞船返回舱成功着陆',
    source: '人民网',
    time: '7 小时',
    grad: 'linear-gradient(135deg,#c0392b,#922b21)',
  },
  {
    title: '女演员长相有多重要？43岁高露给小14岁李昀锐演妈，一出场就让人惊艳',
    source: 'ZAKER娱乐',
    time: '1 天',
    grad: 'linear-gradient(135deg,#5a7a9a,#33536f)',
  },
  {
    title: '曾因言论翻车今又惹怒跑男粉，白鹿一月掉粉百万，郑恺李晨沉默',
    source: '一点资讯',
    time: '17 小时',
    grad: 'linear-gradient(135deg,#a06a6a,#704040)',
  },
]

const hotList = [
  '神21号乘组凯旋 任务圆满成功',
  '榴莲仅退款事件商家已报警',
  '航天员张陆从太空带回一个苹果',
  '演员刘洵去世 罗家英悼念',
  '法拉利电车"撞脸"蔚来萤火虫',
  '不加一滴水雪糕配料表首位是水',
]

export default function DiscoverFeed() {
  return (
    <div className="discover">
      <div className="discover-inner">
        <h2 className="discover-title">发现</h2>
        <div className="feed-grid">
          {cards.map((c) => (
            <article className={`feed-card ${c.tall ? 'tall' : ''}`} key={c.title}>
              <div className="feed-thumb" style={{ background: c.grad }} />
              <div className="feed-body">
                <div className="feed-meta">
                  {c.source} · {c.time}
                </div>
                <div className="feed-title">{c.title}</div>
              </div>
            </article>
          ))}

          <article className="feed-card list-card">
            <div className="list-head">🔥 热榜</div>
            <ol className="list-items">
              {hotList.map((h, i) => (
                <li key={h}>
                  <span className={`rank r${i + 1}`}>{i + 1}</span>
                  {h}
                </li>
              ))}
            </ol>
          </article>

          <article className="feed-card weather-card">
            <div className="weather-top">
              <span>南京市</span>
            </div>
            <div className="weather-now">
              <span className="temp">25°</span>
              <span className="cond">晴 · 快下雨了</span>
            </div>
            <div className="weather-row">
              {[
                ['今天', '27°', '17°'],
                ['周日', '30°', '20°'],
                ['周一', '31°', '22°'],
                ['周二', '32°', '22°'],
                ['周三', '34°', '24°'],
              ].map((d) => (
                <div className="wcol" key={d[0]}>
                  <div>{d[0]}</div>
                  <div className="hi">{d[1]}</div>
                  <div className="lo">{d[2]}</div>
                </div>
              ))}
            </div>
          </article>
        </div>

        <footer className="discover-footer">
          <a href="#" onClick={(e) => e.preventDefault()}>
            隐私与 Cookie
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            法律声明
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            关于我们的广告
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            帮助
          </a>
          <a href="#" onClick={(e) => e.preventDefault()}>
            反馈
          </a>
          <span className="copy">© 2026 Microsoft</span>
        </footer>
      </div>
    </div>
  )
}

===FILE: src/components/DiscoverFeed.css===
.discover {
  background: rgb(236, 236, 236);
  padding: 24px 0 60px;
}

.discover-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 16px;
}

.discover-title {
  font-size: 16px;
  font-weight: 600;
  color: rgb(34, 34, 34);
  margin: 0 0 14px;
}

.feed-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  align-items: start;
}

.feed-card {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.feed-thumb {
  width: 100%;
  height: 150px;
}

.feed-card.tall .feed-thumb {
  height: 230px;
}

.feed-body {
  padding: 12px 14px 16px;
}

.feed-meta {
  font-size: 12.8px;
  color: rgb(76, 76, 76);
  margin-bottom: 6px;
}

.feed-title {
  font-size: 14px;
  line-height: 1.45;
  color: rgb(17, 17, 17);
  font-weight: 600;
}

.list-card {
  padding: 14px 16px;
}

.list-head {
  font-size: 14px;
  font-weight: 600;
  color: rgb(34, 34, 34);
  margin-bottom: 12px;
}

.list-items {
  list-style: none;
  margin: 0;
  padding: 0;
}

.list-items li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: rgb(43, 43, 43);
  padding: 7px 0;
  line-height: 1.3;
}

.rank {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 3px;
  font-size: 12px;
  color: #ffffff;
  background: #b0b0b0;
  flex-shrink: 0;
}

.rank.r1 {
  background: #e5462f;
}
.rank.r2 {
  background: #f0883e;
}
.rank.r3 {
  background: #f5b942;
}

.weather-card {
  padding: 14px 16px;
}

.weather-top {
  font-size: 13px;
  color: rgb(76, 76, 76);
  margin-bottom: 8px;
}

.weather-now {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 14px;
}

.weather-now .temp {
  font-size: 34px;
  font-weight: 600;
  color: rgb(17, 17, 17);
}

.weather-now .cond {
  font-size: 13px;
  color: rgb(76, 76, 76);
}

.weather-row {
  display: flex;
  justify-content: space-between;
  text-align: center;
}

.wcol {
  font-size: 12.8px;
  color: rgb(76, 76, 76);
}

.wcol .hi {
  color: rgb(17, 17, 17);
  font-weight: 600;
  margin-top: 4px;
}

.wcol .lo {
  margin-top: 2px;
}

.discover-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  align-items: center;
  margin-top: 28px;
  padding-top: 16px;
  font-size: 12.8px;
  color: rgb(76, 76, 76);
}

.discover-footer a {
  color: rgb(76, 76, 76);
  text-decoration: none;
}

.discover-footer a:hover {
  text-decoration: underline;
}

.discover-footer .copy {
  margin-left: auto;
}

@media (max-width: 860px) {
  .feed-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .feed-grid {
    grid-template-columns: 1fr;
  }
}

===FILE: src/components/SearchResultsPage.tsx===
import { useMemo } from 'react'
import SearchBar from './SearchBar'
import { MicrosoftLogo } from './icons'
import { generateResults, totalResultCount } from '../data/mockResults'
import './SearchResultsPage.css'

interface Props {
  query: string
  setQuery: (v: string) => void
  submitted: string
  page: number
  onSearch: (q: string) => void
  onNextPage: () => void
  onPrevPage: () => void
  onGoToPage: (p: number) => void
  onHome: () => void
}

export default function SearchResultsPage({
  query,
  setQuery,
  submitted,
  page,
  onSearch,
  onNextPage,
  onPrevPage,
  onGoToPage,
  onHome,
}: Props) {
  const results = useMemo(
    () => generateResults(submitted, page),
    [submitted, page]
  )
  const total = useMemo(() => totalResultCount(submitted), [submitted])

  const pageWindowStart = Math.max(1, page - 2)
  const pageNumbers = Array.from({ length: 5 }, (_, i) => pageWindowStart + i)

  return (
    <div className="results-page">
      <header className="results-header">
        <button className="results-logo" onClick={onHome} aria-label="返回首页">
          <MicrosoftLogo />
          <span>Microsoft Bing</span>
        </button>
        <SearchBar
          query={query}
          setQuery={setQuery}
          onSearch={onSearch}
          variant="compact"
        />
      </header>

      <main className="results-main">
        <section
          className="b_results_wrap"
          data-testid="search-results"
        >
          <div className="results-info">
            约 {total.toLocaleString('zh-CN')} 条结果 · 第 {page} 页
          </div>

          <ol
            id="b_results"
            className="b_results"
            data-testid="result-list"
          >
            {results.map((r, i) => (
              <li className="b_algo" key={`${page}-${i}`}>
                <div className="b_url">{r.displayUrl}</div>
                <h2 className="b_title">
                  <a href="#" onClick={(e) => e.preventDefault()}>
                    {r.title}
                  </a>
                </h2>
                <p className="b_snippet">{r.snippet}</p>
              </li>
            ))}
          </ol>

          <nav className="pagination" aria-label="分页">
            <a
              className="sb_pagP"
              href="#"
              onClick={(e) => {
                e.preventDefault()
                if (page > 1) onPrevPage()
              }}
              aria-disabled={page === 1}
            >
              ‹ 上一页
            </a>
            {pageNumbers.map((p) => (
              <a
                key={p}
                className={`pag-num ${p === page ? 'active' : ''}`}
                href="#"
                onClick={(e) => {
                  e.preventDefault()
                  onGoToPage(p)
                }}
              >
                {p}
              </a>
            ))}
            <a
              className="sb_pagN"
              data-testid="next-page"
              title="下一页"
              aria-label="下一页"
              href="#"
              onClick={(e) => {
                e.preventDefault()
                onNextPage()
              }}
            >
              下一页 ›
            </a>
          </nav>
        </section>
      </main>
    </div>
  )
}

===FILE: src/components/SearchResultsPage.css===
.results-page {
  min-height: 100vh;
  background: #ffffff;
}

.results-header {
  display: flex;
  align-items: center;
  gap: 28px;
  padding: 14px 28px;
  border-bottom: 1px solid rgb(236, 236, 236);
  background: #ffffff;
  position: sticky;
  top: 0;
  z-index: 5;
}

.results-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 20px;
  font-weight: 600;
  color: rgb(17, 17, 17);
  white-space: nowrap;
}

.results-main {
  max-width: 1000px;
  margin: 0 auto;
  padding: 22px 28px 60px;
}

.results-info {
  font-size: 13px;
  color: rgb(118, 118, 118);
  margin-bottom: 18px;
}

.b_results {
  list-style: none;
  margin: 0;
  padding: 0;
  max-width: 640px;
}

.b_algo {
  margin-bottom: 24px;
}

.b_url {
  font-size: 13px;
  color: rgb(76, 76, 76);
  margin-bottom: 3px;
  word-break: break-all;
}

.b_title {
  margin: 0 0 4px;
  font-size: 20px;
  font-weight: 400;
  line-height: 1.3;
}

.b_title a {
  color: #1a0dab;
  text-decoration: none;
}

.b_title a:hover {
  text-decoration: underline;
}

.b_snippet {
  margin: 0;
  font-size: 14px;
  line-height: 1.55;
  color: rgb(43, 43, 43);
}

.pagination {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 32px;
  max-width: 640px;
  flex-wrap: wrap;
}

.pagination a {
  text-decoration: none;
  color: #0f6cbd;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 4px;
}

.pagination a:hover {
  background: rgb(236, 236, 236);
}

.pagination .pag-num.active {
  background: #0f6cbd;
  color: #ffffff;
  font-weight: 600;
}

.pagination .sb_pagN {
  font-weight: 600;
}

@media (max-width: 680px) {
  .results-header {
    gap: 14px;
    padding: 12px 16px;
  }
  .results-logo span {
    display: none;
  }
  .results-main {
    padding: 18px 16px 40px;
  }
}