import { useQuery } from 'react-query'
import { useParams, Link } from 'react-router-dom'
import { articlesApi } from '../services/api'
import { ArrowLeftIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline'

export default function ArticleDetail() {
  const { id } = useParams<{ id: string }>()
  const articleId = parseInt(id || '0')

  const { data: article, isLoading } = useQuery(
    ['article', articleId],
    () => articlesApi.getById(articleId).then((res) => res.data),
    { enabled: !!articleId }
  )

  if (isLoading) {
    return <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
  }

  if (!article) {
    return <div className="text-center py-12">
      <p className="text-gray-500">Article not found</p>
    </div>
  }

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <Link
        to="/articles"
        className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeftIcon className="h-4 w-4 mr-2" />
        Back to articles
      </Link>

      {/* Article Header */}
      <div className="bg-white p-8 rounded-lg shadow">
        {/* Badges */}
        <div className="flex items-center gap-2 mb-4">
          {article.is_featured && (
            <span className="px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
              Featured
            </span>
          )}
          {article.is_emerging && (
            <span className="px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
              Emerging Trend
            </span>
          )}
          {article.primary_theme && (
            <span
              className="px-3 py-1 rounded-full text-sm font-medium"
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
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {article.title}
        </h1>

        {/* Metadata */}
        <div className="flex items-center gap-6 text-sm text-gray-600 mb-6 pb-6 border-b border-gray-200">
          <span className="font-medium">{article.source}</span>
          {article.author && <span>By {article.author}</span>}
          <span>{new Date(article.published_date).toLocaleDateString()}</span>
          {article.region && <span>{article.region}</span>}
          {article.view_count > 0 && <span>{article.view_count} views</span>}
        </div>

        {/* Summary */}
        {article.summary && (
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Executive Summary
            </h2>
            <p className="text-gray-700 leading-relaxed">
              {article.summary}
            </p>
          </div>
        )}

        {/* Key Takeaways */}
        {article.key_takeaways && article.key_takeaways.length > 0 && (
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Key Takeaways
            </h2>
            <ul className="space-y-2">
              {article.key_takeaways.map((takeaway, i) => (
                <li key={i} className="flex items-start">
                  <span className="flex-shrink-0 h-6 w-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-sm font-medium mr-3">
                    {i + 1}
                  </span>
                  <span className="text-gray-700 pt-0.5">{takeaway}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Analysis Metrics */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          {article.signal_strength !== null && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-500 mb-1">Signal Strength</div>
              <div className="text-2xl font-bold text-indigo-600">
                {(article.signal_strength * 100).toFixed(0)}%
              </div>
            </div>
          )}

          {article.sentiment_label && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-500 mb-1">Sentiment</div>
              <div className={`text-2xl font-bold capitalize ${
                article.sentiment_label === 'positive' ? 'text-green-600' :
                article.sentiment_label === 'negative' ? 'text-red-600' :
                'text-gray-600'
              }`}>
                {article.sentiment_label}
              </div>
            </div>
          )}

          {article.confidence_score !== null && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-500 mb-1">AI Confidence</div>
              <div className="text-2xl font-bold text-indigo-600">
                {(article.confidence_score * 100).toFixed(0)}%
              </div>
            </div>
          )}
        </div>

        {/* Themes and Sectors */}
        <div className="flex items-start gap-8 mb-6">
          {article.themes && article.themes.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">Themes</h3>
              <div className="flex flex-wrap gap-2">
                {article.themes.map((theme) => (
                  <span
                    key={theme.id}
                    className="px-3 py-1 rounded-full text-sm"
                    style={{
                      backgroundColor: `${theme.color}20`,
                      color: theme.color || '#3B82F6',
                    }}
                  >
                    {theme.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {article.sectors && article.sectors.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">Sectors</h3>
              <div className="flex flex-wrap gap-2">
                {article.sectors.map((sector) => (
                  <span
                    key={sector.id}
                    className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm"
                  >
                    {sector.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Read Original Button */}
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Read Original Article
          <ArrowTopRightOnSquareIcon className="ml-2 h-4 w-4" />
        </a>
      </div>
    </div>
  )
}
