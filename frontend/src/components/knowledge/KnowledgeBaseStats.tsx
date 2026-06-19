import React from 'react';
import type { DocumentResponse } from '../../types/knowledge';

interface Props {
  documents: DocumentResponse[];
}

const KnowledgeBaseStats: React.FC<Props> = ({ documents }) => {
  const total = documents.length;
  const active = documents.filter(d => d.status === 'active').length;
  const archived = documents.filter(d => d.status === 'archived').length;
  const deleted = documents.filter(d => d.status === 'deleted').length;

  const stats = [
    { label: 'Total Documents', value: total, color: 'text-blue-600', bg: 'bg-blue-50' },
    { label: 'Active', value: active, color: 'text-green-600', bg: 'bg-green-50' },
    { label: 'Archived', value: archived, color: 'text-yellow-600', bg: 'bg-yellow-50' },
    { label: 'Deleted', value: deleted, color: 'text-red-600', bg: 'bg-red-50' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, idx) => (
        <div key={idx} className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow">
          <div className="flex items-center space-x-3 mb-2">
            <div className={`p-2 rounded-lg ${stat.bg}`}>
              <svg className={`w-5 h-5 ${stat.color}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            </div>
            <h3 className="text-sm font-medium text-gray-500">{stat.label}</h3>
          </div>
          <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
        </div>
      ))}
    </div>
  );
};

export default KnowledgeBaseStats;
