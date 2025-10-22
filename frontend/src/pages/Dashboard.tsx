import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import {
  ArrowTrendingUpIcon,
  NewspaperIcon,
  LightBulbIcon,
  FireIcon,
} from '@heroicons/react/24/outline'
import { statsApi, articlesApi, trendsApi, insightsApi } from '../services/api'

const THEME_COLORS = [
  '#3B82F6', '#8B5CF6', '#10B981', '#F59E0B',
  '#EF4444', '#06B6D4', '#EC4899', '#6366F1',
]

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery('stats', () =>
    statsApi.get().then((res) => res.data)
  )

  const { data: featuredArticles } = useQuery('featured-articles', () =>
    articlesApi.getFeatured(5).then((res) => res.data)
  )

  const { data: emergingTrends } = useQuery('emerging-trends', () =>
    trendsApi.getEmerging(5).then((res) => res.data)
  )

  const { data: topInsights } = useQuery('top-insights', () =>
    insightsApi.getAll(0, 5, 'high').then((res) => res.data)
  )

  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          HR Signals Command Centre
        </h1>
        <p className="mt-2 text-gray-600">
          Your intelligence layer for HR and workforce transformation
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Articles"
          value={stats?.total_articles || 0}
          icon={NewspaperIcon}
          color="bg-blue-500"
          subtitle={`${stats?.recent_articles || 0} this week`}
        />
        <StatCard
          title="Active Trends"
          value={stats?.total_trends || 0}
          icon={ArrowTrendingUpIcon}
          color="bg-purple-500"
          subtitle={`${stats?.emerging_trends || 0} emerging`}
        />
        <StatCard
          title="Key Insights"
          value={stats?.total_insights || 0}
          icon={LightBulbIcon}
          color="bg-green-500"
          subtitle="Extracted this month"
        />
        <StatCard
          title="Signal Strength"
          value="High"
          icon={FireIcon}
          color="bg-orange-500"
          subtitle="Market activity"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Theme Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Content by Theme
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats?.theme_distribution || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="theme"
                angle={-45}
                textAnchor="end"
                height={100}
                fontSize={12}
              />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Sentiment Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Sentiment Analysis
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={stats?.sentiment_distribution || []}
                dataKey="count"
                nameKey="sentiment"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {(stats?.sentiment_distribution || []).map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={
                      entry.sentiment === 'positive'
                        ? '#10B981'
                        : entry.sentiment === 'negative'
                        ? '#EF4444'
                        : '#6B7280'
                    }
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Featured Articles */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Featured Stories
            </h2>
          </div>
          <div className="divide-y divide-gray-200">
            {featuredArticles?.map((article) => (
              <Link
                key={article.id}
                to={`/articles/${article.id}`}
                className="block p-4 hover:bg-gray-50 transition"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-gray-900 mb-1">
                      {article.title}
                    </h3>
                    <p className="text-xs text-gray-500">
                      {article.source} • {new Date(article.published_date).toLocaleDateString()}
                    </p>
                    {article.primary_theme && (
                      <span className="inline-block mt-2 px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                        {article.primary_theme}
                      </span>
                    )}
                  </div>
                  {article.signal_strength && (
                    <div className="ml-4 flex-shrink-0">
                      <SignalStrength value={article.signal_strength} />
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
          <div className="p-4 border-t border-gray-200">
            <Link
              to="/articles?featured=true"
              className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              View all featured articles →
            </Link>
          </div>
        </div>

        {/* Emerging Trends */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Emerging Trends
            </h2>
          </div>
          <div className="divide-y divide-gray-200">
            {emergingTrends?.map((trend) => (
              <div key={trend.id} className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-gray-900 mb-1">
                      {trend.name}
                    </h3>
                    <p className="text-xs text-gray-600 mb-2">
                      {trend.description}
                    </p>
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <span>{trend.article_count} articles</span>
                      {trend.momentum && (
                        <span className="flex items-center text-green-600">
                          <ArrowTrendingUpIcon className="h-3 w-3 mr-1" />
                          {(trend.momentum * 100).toFixed(0)}% momentum
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="p-4 border-t border-gray-200">
            <Link
              to="/trends?status=emerging"
              className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              View all emerging trends →
            </Link>
          </div>
        </div>
      </div>

      {/* Top Insights */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            High-Impact Insights
          </h2>
        </div>
        <div className="divide-y divide-gray-200">
          {topInsights?.map((insight) => (
            <div key={insight.id} className="p-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-yellow-100 flex items-center justify-center">
                    <LightBulbIcon className="h-5 w-5 text-yellow-600" />
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <h3 className="text-sm font-medium text-gray-900 mb-1">
                    {insight.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-2">
                    {insight.description}
                  </p>
                  <div className="flex items-center gap-3 text-xs text-gray-500">
                    {insight.impact_level && (
                      <span className="px-2 py-1 rounded-full bg-red-100 text-red-800">
                        {insight.impact_level} impact
                      </span>
                    )}
                    {insight.time_horizon && (
                      <span>{insight.time_horizon}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="p-4 border-t border-gray-200">
          <Link
            to="/insights"
            className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            View all insights →
          </Link>
        </div>
      </div>
    </div>
  )
}

// Helper Components
function StatCard({ title, value, icon: Icon, color, subtitle }: any) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`${color} rounded-md p-3`}>
              <Icon className="h-6 w-6 text-white" />
            </div>
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">
                {title}
              </dt>
              <dd className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {value}
                </div>
              </dd>
              {subtitle && (
                <dd className="text-xs text-gray-500 mt-1">{subtitle}</dd>
              )}
            </dl>
          </div>
        </div>
      </div>
    </div>
  )
}

function SignalStrength({ value }: { value: number }) {
  const bars = Math.round(value * 5)
  return (
    <div className="flex items-center gap-0.5">
      {[...Array(5)].map((_, i) => (
        <div
          key={i}
          className={`w-1 h-${(i + 1) * 2} ${
            i < bars ? 'bg-green-500' : 'bg-gray-300'
          }`}
        />
      ))}
    </div>
  )
}
