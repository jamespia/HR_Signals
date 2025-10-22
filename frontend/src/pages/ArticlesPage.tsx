import { useState } from 'react'
import { useQuery } from 'react-query'
import { Link } from 'react-router-dom'
import { articlesApi, themesApi, type ArticleFilters } from '../services/api'
import { FunnelIcon, ArrowUpIcon } from '@heroicons/react/24/outline'

export default function ArticlesPage() {
  const [filters, setFilters] = useState<ArticleFilters>({
    skip: 0,
    limit: 20,
  })

  const { data: articles, isLoading } = useQuery(
    ['articles', filters],
    () => articlesApi.getAll(filters).then((res) => res.data),
    { keepPreviousData: true }
  )

  const { data: themes } = useQuery('themes', () =>
    themesApi.getAll().then((res) => res.data)
  )

  const handleFilterChange = (key: keyof ArticleFilters, value: any) => {
    setFilters((prev) => ({ ...prev, [key]: value, skip: 0 }))
  }

  const handleLoadMore = () => {
    setFilters((prev) => ({ ...prev, skip: (prev.skip || 0) + 20 }))
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Articles</h1>
          <p className="mt-2 text-gray-600">
            Browse and filter the latest HR and workforce news
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center gap-2 mb-4">
          <FunnelIcon className="h-5 w-5 text-gray-400" />
          <h2 className="text-sm font-medium text-gray-900">Filters</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Theme Filter */}
          <select
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={filters.theme || ''}
            onChange={(e) => handleFilterChange('theme', e.target.value || undefined)}
          >
            <option value="">All Themes</option>
            {themes?.map((theme) => (
              <option key={theme.id} value={theme.name}>
                {theme.name}
              </option>
            ))}
          </select>

          {/* Region Filter */}
          <select
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={filters.region || ''}
            onChange={(e) => handleFilterChange('region', e.target.value || undefined)}
          >
            <option value="">All Regions</option>
            <option value="Global">Global</option>
            <option value="Australia">Australia</option>
            <option value="Asia Pacific">Asia Pacific</option>
            <option value="North America">North America</option>
            <option value="Europe">Europe</option>
            <option value="UK">UK</option>
          </select>

          {/* Featured Filter */}
          <select
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={filters.is_featured !== undefined ? String(filters.is_featured) : ''}
            onChange={(e) =>
              handleFilterChange(
                'is_featured',
                e.target.value === '' ? undefined : e.target.value === 'true'
              )
            }
          >
            <option value="">All Articles</option>
            <option value="true">Featured Only</option>
            <option value="false">Non-Featured</option>
          </select>

          {/* Signal Strength Filter */}
          <select
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={filters.min_signal_strength || ''}
            onChange={(e) =>
              handleFilterChange(
                'min_signal_strength',
                e.target.value ? parseFloat(e.target.value) : undefined
              )
            }
          >
            <option value="">Any Signal</option>
            <option value="0.8">High (0.8+)</option>
            <option value="0.6">Medium (0.6+)</option>
            <option value="0.4">Low (0.4+)</option>
          </select>
        </div>
      </div>

      {/* Articles List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        ) : articles && articles.length > 0 ? (
          <>
            {articles.map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}

            {/* Load More Button */}
            {articles.length >= (filters.limit || 20) && (
              <div className="flex justify-center pt-4">
                <button
                  onClick={handleLoadMore}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Load More
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">No articles found matching your filters.</p>
          </div>
        )}
      </div>
    </div>
  )
}

function ArticleCard({ article }: { article: any }) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))

    if (diffHours < 24) {
      return `${diffHours}h ago`
    } else if (diffHours < 48) {
      return 'Yesterday'
    } else {
      return date.toLocaleDateString()
    }
  }

  return (
    <Link to={`/articles/${article.id}`}>
      <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition cursor-pointer">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            {/* Badges */}
            <div className="flex items-center gap-2 mb-2">
              {article.is_featured && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                  Featured
                </span>
              )}
              {article.is_emerging && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  <ArrowUpIcon className="h-3 w-3 mr-1" />
                  Emerging
                </span>
              )}
              {article.primary_theme && (
                <span
                  className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                  style={{
                    backgroundColor: `${article.themes[0]?.color}20`,
                    color: article.themes[0]?.color || '#3B82F6',
                  }}
                >
                  {article.primary_theme}
                </span>
              )}
            </div>

            {/* Title */}
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {article.title}
            </h3>

            {/* Summary */}
            {article.summary && (
              <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                {article.summary}
              </p>
            )}

            {/* Key Takeaways */}
            {article.key_takeaways && article.key_takeaways.length > 0 && (
              <div className="mb-3">
                <h4 className="text-xs font-medium text-gray-700 mb-1">
                  Key Takeaways:
                </h4>
                <ul className="list-disc list-inside text-xs text-gray-600 space-y-1">
                  {article.key_takeaways.slice(0, 2).map((takeaway: string, i: number) => (
                    <li key={i}>{takeaway}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Metadata */}
            <div className="flex items-center gap-4 text-xs text-gray-500">
              <span className="font-medium">{article.source}</span>
              <span>{formatDate(article.published_date)}</span>
              {article.region && <span>{article.region}</span>}
              {article.sentiment_label && (
                <span
                  className={`px-2 py-1 rounded-full ${
                    article.sentiment_label === 'positive'
                      ? 'bg-green-100 text-green-800'
                      : article.sentiment_label === 'negative'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {article.sentiment_label}
                </span>
              )}
            </div>
          </div>

          {/* Signal Strength Indicator */}
          {article.signal_strength !== null && (
            <div className="ml-6 flex-shrink-0">
              <div className="text-center">
                <div className="text-2xl font-bold text-indigo-600">
                  {(article.signal_strength * 100).toFixed(0)}
                </div>
                <div className="text-xs text-gray-500">Signal</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </Link>
  )
}
