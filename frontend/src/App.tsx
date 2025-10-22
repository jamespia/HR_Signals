import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ArticlesPage from './pages/ArticlesPage'
import TrendsPage from './pages/TrendsPage'
import InsightsPage from './pages/InsightsPage'
import DigestsPage from './pages/DigestsPage'
import ArticleDetail from './pages/ArticleDetail'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/articles" element={<ArticlesPage />} />
          <Route path="/articles/:id" element={<ArticleDetail />} />
          <Route path="/trends" element={<TrendsPage />} />
          <Route path="/insights" element={<InsightsPage />} />
          <Route path="/digests" element={<DigestsPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
