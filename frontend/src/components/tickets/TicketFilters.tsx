import React from 'react';
import { Search, Filter } from 'lucide-react';
import type { TicketStatus } from '../../types/ticket';

interface TicketFiltersProps {
  searchQuery: string;
  onSearchChange: (query: string) => void;
  statusFilter: TicketStatus | 'all';
  onStatusFilterChange: (status: TicketStatus | 'all') => void;
}

const TicketFilters: React.FC<TicketFiltersProps> = ({
  searchQuery,
  onSearchChange,
  statusFilter,
  onStatusFilterChange
}) => {
  return (
    <div className="flex flex-col sm:flex-row gap-4 mb-6">
      <div className="relative flex-1">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          placeholder="Search by ID or question..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          className="block w-full pl-10 pr-3 py-2 border border-gray-200 rounded-lg leading-5 bg-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition-all"
        />
      </div>
      
      <div className="relative min-w-[200px]">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Filter className="h-5 w-5 text-gray-400" />
        </div>
        <select
          value={statusFilter}
          onChange={(e) => onStatusFilterChange(e.target.value as TicketStatus | 'all')}
          className="block w-full pl-10 pr-10 py-2 text-base border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-lg appearance-none bg-white cursor-pointer"
        >
          <option value="all">All Statuses</option>
          <option value="open">Open</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default TicketFilters;
