import React from 'react';
import type { ProfileStats as ProfileStatsType } from '../../types/profile';
import { MessageSquare, Ticket, CheckCircle, Clock } from 'lucide-react';

interface ProfileStatsProps {
  stats: ProfileStatsType | null;
  loading: boolean;
}

const ProfileStats: React.FC<ProfileStatsProps> = ({ stats, loading }) => {
  if (loading || !stats) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="bg-white rounded-2xl p-6 border border-gray-200 animate-pulse">
            <div className="h-10 w-10 bg-gray-200 rounded-lg mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          </div>
        ))}
      </div>
    );
  }

  const statCards = [
    { name: 'Total Conversations', value: stats.totalConversations, icon: MessageSquare, color: 'text-blue-600', bg: 'bg-blue-50' },
    { name: 'Open Tickets', value: stats.openTickets, icon: Ticket, color: 'text-amber-600', bg: 'bg-amber-50' },
    { name: 'Resolved Tickets', value: stats.resolvedTickets, icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-50' },
    { name: 'Avg Response Time', value: stats.averageResponseTime, icon: Clock, color: 'text-purple-600', bg: 'bg-purple-50' },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {statCards.map((stat) => {
        const Icon = stat.icon;
        return (
          <div key={stat.name} className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm transition-all hover:shadow-md">
            <div className={`inline-flex p-3 rounded-xl ${stat.bg} ${stat.color} mb-4`}>
              <Icon className="w-6 h-6" />
            </div>
            <h3 className="text-sm font-medium text-gray-500 mb-1">{stat.name}</h3>
            <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
          </div>
        );
      })}
    </div>
  );
};

export default ProfileStats;
