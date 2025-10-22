import { useQuery } from 'react-query'
import { trendsApi } from '../services/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { ArrowTrendingUpIcon } from '@heroicons/react/24/outline'

export default function TrendsPage() {
  const { data: trends, isLoading } = useQuery('all-trends', () =>
    trendsApi.getAll().then((res) => res.data)
  )

  if (isLoading) {
    return <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Trends</h1>
        <p className="mt-2 text-gray-600">
          Track emerging and evolving trends in HR and workforce transformation
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {trends?.map((trend) => (
          <div key={trend.id} className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h3 className="text-xl font-semibold text-gray-900">{trend.name}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    trend.status === 'emerging' ? 'bg-green-100 text-green-800' :
                    trend.status === 'growing' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {trend.status}
                  </span>
                </div>
                <p className="text-gray-600 mb-3">{trend.description}</p>

                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>{trend.article_count} articles</span>
                  {trend.momentum && (
                    <span className="flex items-center text-green-600">
                      <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
                      {(trend.momentum * 100).toFixed(0)}% momentum
                    </span>
                  )}
                  <span>{trend.region}</span>
                </div>
              </div>
            </div>

            {/* Trend Chart */}
            {trend.data_points && trend.data_points.length > 0 && (
              <div className="mt-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Activity Over Time</h4>
                <ResponsiveContainer width="100%" height={150}>
                  <LineChart data={trend.data_points}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="date"
                      tickFormatter={(value) => new Date(value).toLocaleDateString()}
                      fontSize={12}
                    />
                    <YAxis fontSize={12} />
                    <Tooltip
                      labelFormatter={(value) => new Date(value).toLocaleDateString()}
                    />
                    <Line
                      type="monotone"
                      dataKey="article_count"
                      stroke="#3B82F6"
                      strokeWidth={2}
                      name="Articles"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
