import Header from './components/Header'
import Breadcrumb from './components/Breadcrumb'
import LeftSidebar from './components/LeftSidebar'
import Content from './components/Content'
import TableOfContents from './components/TableOfContents'
import './styles/app.css'

export default function App() {
  return (
    <>
      <a className="skip-link" href="#content" data-testid="skip-to-content">
        Skip to main content
      </a>
      <Header />
      <div className="page">
        <LeftSidebar />
        <main className="main-area" id="content">
          <article className="article">
            <Breadcrumb />
            <Content />
          </article>
          <TableOfContents />
        </main>
      </div>
    </>
  )
}
