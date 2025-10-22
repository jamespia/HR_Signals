import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface Article {
  id: number
  title: string
  url: string
  source: string
  source_type: string
  author?: string
  published_date: string
  scraped_date: string
  summary?: string
  key_takeaways?: string[]
  primary_theme?: string
  confidence_score?: number
  region?: string
  sentiment_score?: number
  sentiment_label?: string
  signal_strength?: number
  is_featured: boolean
  is_emerging: boolean
  view_count: number
  themes: Theme[]
  sectors: Sector[]
}

export interface Theme {
  id: number
  name: string
  description?: string
  keywords?: string[]
  color?: string
}

export interface Sector {
  id: number
  name: string
  description?: string
}

export interface Insight {
  id: number
  article_id: number
  title: string
  description: string
  impact_level?: string
  time_horizon?: string
  created_date: string
  relevance_score?: number
}

export interface Trend {
  id: number
  name: string
  description?: string
  keywords?: string[]
  start_date: string
  last_updated: string
  article_count: number
  momentum?: number
  status?: string
  region?: string
  data_points: TrendDataPoint[]
}

export interface TrendDataPoint {
  date: string
  article_count: number
  sentiment_avg?: number
  signal_strength_avg?: number
}

export interface Digest {
  id: number
  digest_type: string
  period_start: string
  period_end: string
  created_date: string
  title?: string
  summary?: string
  top_stories?: any[]
  emerging_trends?: string[]
  key_insights?: any[]
  total_articles?: number
  themes_covered?: string[]
  regions_covered?: string[]
}

export interface Stats {
  total_articles: number
  recent_articles: number
  total_insights: number
  total_trends: number
  emerging_trends: number
  theme_distribution: { theme: string; count: number }[]
  sentiment_distribution: { sentiment: string; count: number }[]
}

export interface ArticleFilters {
  skip?: number
  limit?: number
  theme?: string
  sector?: string
  region?: string
  start_date?: string
  end_date?: string
  search?: string
  is_featured?: boolean
  is_emerging?: boolean
  min_signal_strength?: number
}

// API functions
export const articlesApi = {
  getAll: (filters?: ArticleFilters) =>
    api.get<Article[]>('/articles', { params: filters }),

  getById: (id: number) =>
    api.get<Article>(`/articles/${id}`),

  getFeatured: (limit = 10) =>
    api.get<Article[]>('/articles/featured', { params: { limit } }),

  search: (query: string, limit = 20) =>
    api.get('/search', { params: { q: query, limit } }),
}

export const themesApi = {
  getAll: () =>
    api.get<Theme[]>('/themes'),

  getArticles: (themeId: number, limit = 20) =>
    api.get<Article[]>(`/themes/${themeId}/articles`, { params: { limit } }),
}

export const insightsApi = {
  getAll: (skip = 0, limit = 20, impactLevel?: string) =>
    api.get<Insight[]>('/insights', {
      params: { skip, limit, impact_level: impactLevel }
    }),
}

export const trendsApi = {
  getAll: (status?: string, themeId?: number) =>
    api.get<Trend[]>('/trends', { params: { status, theme_id: themeId } }),

  getEmerging: (limit = 10) =>
    api.get<Trend[]>('/trends/emerging', { params: { limit } }),
}

export const digestsApi = {
  getAll: (digestType?: string, limit = 10) =>
    api.get<Digest[]>('/digests', { params: { digest_type: digestType, limit } }),

  getLatest: (digestType = 'daily') =>
    api.get<Digest>('/digests/latest', { params: { digest_type: digestType } }),
}

export const statsApi = {
  get: () =>
    api.get<Stats>('/stats'),
}

export default api
