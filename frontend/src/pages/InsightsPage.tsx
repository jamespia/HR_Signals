import { useQuery } from 'react-query'
import { insightsApi } from '../services/api'
import { LightBulbIcon } from '@heroicons/react/24/outline'

export default function InsightsPage() {
  const { data: insights, isLoading } = useQuery('all-insights', () =>
    insightsApi.getAll(0, 50).then((res) => res.data)
  )

  if (isLoading) {
    return <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Insights</h1>
        <p className="mt-2 text-gray-600">
          AI-extracted strategic insights for HR leaders
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {insights?.map((insight) => (
          <div key={insight.id} className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <div className={`h-10 w-10 rounded-full flex items-center justify-center ${
                  insight.impact_level === 'high' ? 'bg-red-100' :
                  insight.impact_level === 'medium' ? 'bg-yellow-100' :
                  'bg-blue-100'
                }`}>
                  <LightBulbIcon className={`h-6 w-6 ${
                    insight.impact_level === 'high' ? 'text-red-600' :
                    insight.impact_level === 'medium' ? 'text-yellow-600' :
                    'text-blue-600'
                  }`} />
                </div>
              </div>

              <div className="ml-4 flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {insight.title}
                </h3>
                <p className="text-gray-600 mb-3">
                  {insight.description}
                </p>

                <div className="flex items-center gap-3 text-sm">
                  {insight.impact_level && (
                    <span className={`px-3 py-1 rounded-full font-medium ${
                      insight.impact_level === 'high' ? 'bg-red-100 text-red-800' :
                      insight.impact_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {insight.impact_level} impact
                    </span>
                  )}
                  {insight.time_horizon && (
                    <span className="text-gray-500">{insight.time_horizon}</span>
                  )}
                  {insight.relevance_score && (
                    <span className="text-gray-500">
                      Relevance: {(insight.relevance_score * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
