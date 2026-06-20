import React, { useState, useEffect } from 'react';
import { feedbackService } from '../services/feedbackService';
import type { FeedbackResponse, FeedbackStats } from '../types/feedback';
import {
  ThumbsUp,
  ThumbsDown,
  BarChart3,
  MessageSquare,
  Loader2,
  TrendingUp,
  TrendingDown,
} from 'lucide-react';

const FeedbackPage: React.FC = () => {
  const [stats, setStats] = useState<FeedbackStats | null>(null);
  const [feedback, setFeedback] = useState<FeedbackResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const [statsData, feedbackData] = await Promise.all([
          feedbackService.getFeedbackStats(),
          feedbackService.getFeedback(),
        ]);
        setStats(statsData);
        setFeedback(feedbackData);
      } catch (error) {
        console.error('Failed to fetch feedback data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-24">
        <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Feedback Analytics</h1>
        <p className="mt-1 text-sm text-gray-500">
          Monitor user satisfaction and response quality across all agents.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Total Feedback */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-blue-50 rounded-md p-3">
              <MessageSquare className="h-6 w-6 text-blue-600" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Total Feedback</dt>
                <dd className="text-2xl font-semibold text-gray-900">{stats?.total ?? 0}</dd>
              </dl>
            </div>
          </div>
        </div>

        {/* Helpful % */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-50 rounded-md p-3">
              <TrendingUp className="h-6 w-6 text-green-600" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Helpful</dt>
                <dd className="flex items-baseline gap-2">
                  <span className="text-2xl font-semibold text-gray-900">{stats?.helpful_pct ?? 0}%</span>
                  <span className="text-sm text-green-600 font-medium">({stats?.helpful ?? 0})</span>
                </dd>
              </dl>
            </div>
          </div>
        </div>

        {/* Not Helpful % */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-red-50 rounded-md p-3">
              <TrendingDown className="h-6 w-6 text-red-500" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Not Helpful</dt>
                <dd className="flex items-baseline gap-2">
                  <span className="text-2xl font-semibold text-gray-900">{stats?.not_helpful_pct ?? 0}%</span>
                  <span className="text-sm text-red-500 font-medium">({stats?.not_helpful ?? 0})</span>
                </dd>
              </dl>
            </div>
          </div>
        </div>

        {/* By Agent Card */}
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-purple-50 rounded-md p-3">
              <BarChart3 className="h-6 w-6 text-purple-600" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Active Agents</dt>
                <dd className="text-2xl font-semibold text-gray-900">
                  {stats?.by_agent ? Object.keys(stats.by_agent).length : 0}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Breakdown */}
      {stats?.by_agent && Object.keys(stats.by_agent).length > 0 && (
        <div className="bg-white shadow-sm rounded-xl border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-lg font-medium text-gray-900">Feedback by Agent</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(stats.by_agent).map(([agent, data]) => {
                const total = data.helpful + data.not_helpful;
                const helpfulPct = total > 0 ? Math.round((data.helpful / total) * 100) : 0;
                return (
                  <div key={agent} className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-semibold text-gray-800 capitalize">{agent}</span>
                      <span className="text-xs text-gray-500">{total} total</span>
                    </div>
                    {/* Progress bar */}
                    <div className="w-full bg-red-100 rounded-full h-2.5 overflow-hidden">
                      <div
                        className="bg-green-500 h-2.5 rounded-full transition-all duration-500"
                        style={{ width: `${helpfulPct}%` }}
                      />
                    </div>
                    <div className="flex justify-between mt-2 text-xs">
                      <span className="text-green-600 font-medium flex items-center gap-1">
                        <ThumbsUp className="w-3 h-3" /> {data.helpful}
                      </span>
                      <span className="text-red-500 font-medium flex items-center gap-1">
                        <ThumbsDown className="w-3 h-3" /> {data.not_helpful}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Feedback Table */}
      <div className="bg-white shadow-sm rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100">
          <h2 className="text-lg font-medium text-gray-900">Recent Feedback</h2>
        </div>

        {feedback.length === 0 ? (
          <div className="px-6 py-12 text-center text-sm text-gray-500">
            No feedback received yet.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Agent</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Feedback</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Comment</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Question</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-100">
                {feedback.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(item.created_at).toLocaleDateString([], {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                      })}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 font-medium">
                      User #{item.user_id ?? '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 capitalize">
                        {item.route_selected || 'unknown'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {item.feedback_type === 'helpful' ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-green-50 text-green-700">
                          <ThumbsUp className="w-3 h-3" /> Helpful
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-red-50 text-red-600">
                          <ThumbsDown className="w-3 h-3" /> Not Helpful
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                      {item.feedback_comment || '—'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 max-w-sm truncate">
                      {item.question}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default FeedbackPage;
