import React from 'react';

interface Props {
  status: 'pending' | 'processing' | 'active' | 'archived' | 'deleted' | 'failed';
  version: string;
}

const DocumentVersionBadge: React.FC<Props> = ({ status, version }) => {
  const getStatusColor = () => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'processing': return 'bg-blue-100 text-blue-800 border-blue-200 animate-pulse';
      case 'active': return 'bg-green-100 text-green-800 border-green-200';
      case 'archived': return 'bg-gray-100 text-gray-800 border-gray-200';
      case 'failed': return 'bg-red-100 text-red-800 border-red-200';
      case 'deleted': return 'bg-red-100 text-red-800 border-red-200 opacity-50';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getStatusColor()}`}>
        {status.toUpperCase()}
      </span>
      <span className="text-sm font-semibold text-gray-600 bg-gray-100 px-2 py-1 rounded-md">
        {version}
      </span>
    </div>
  );
};

export default DocumentVersionBadge;
