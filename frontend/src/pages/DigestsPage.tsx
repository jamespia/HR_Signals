import { useQuery } from 'react-query'
import { digestsApi } from '../services/api'
import { DocumentTextIcon } from '@heroicons/react/24/outline'

export default function DigestsPage() {
  const { data: digests, isLoading } = useQuery('all-digests', () =>
    digestsApi.getAll(undefined, 20).then((res) => res.data)
  )

  if (isLoading) {
    return <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Digests</h1>
        <p className="mt-2 text-gray-600">
          Executive summaries and curated insights
        </p>
      </div>

      <div className="space-y-6">
        {digests?.map((digest) => (
          <div key={digest.id} className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <DocumentTextIcon className="h-6 w-6 text-indigo-600 mr-3" />
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">
                    {digest.title || `${digest.digest_type} Digest`}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {new Date(digest.period_start).toLocaleDateString()} -{' '}
                    {new Date(digest.period_end).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                digest.digest_type === 'daily' ? 'bg-blue-100 text-blue-800' :
                'bg-purple-100 text-purple-800'
              }`}>
                {digest.digest_type}
              </span>
            </div>

            {digest.summary && (
              <p className="text-gray-700 mb-4">{digest.summary}</p>
            )}

            {digest.top_stories && digest.top_stories.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-900 mb-2">
                  Top Stories
                </h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {digest.top_stories.map((story, i) => (
                    <li key={i}>{story}</li>
                  ))}
                </ul>
              </div>
            )}

            {digest.emerging_trends && digest.emerging_trends.length > 0 && (
              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-900 mb-2">
                  Emerging Trends
                </h4>
                <div className="flex flex-wrap gap-2">
                  {digest.emerging_trends.map((trend, i) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                    >
                      {trend}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {digest.key_insights && digest.key_insights.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-gray-900 mb-2">
                  Strategic Implications
                </h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {digest.key_insights.map((insight, i) => (
                    <li key={i}>{insight}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-4 pt-4 border-t border-gray-200 flex items-center gap-4 text-xs text-gray-500">
              {digest.total_articles && (
                <span>{digest.total_articles} articles analyzed</span>
              )}
              {digest.themes_covered && digest.themes_covered.length > 0 && (
                <span>{digest.themes_covered.length} themes</span>
              )}
              {digest.regions_covered && digest.regions_covered.length > 0 && (
                <span>{digest.regions_covered.length} regions</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
