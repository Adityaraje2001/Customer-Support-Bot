import React from 'react';
import { Search } from 'lucide-react';
import type { ConversationFilter } from '../../types/conversation';

interface ConversationFiltersProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
  activeFilter: ConversationFilter;
  onFilterChange: (filter: ConversationFilter) => void;
}

const ConversationFilters: React.FC<ConversationFiltersProps> = ({ 
  searchTerm, 
  onSearchChange, 
  activeFilter, 
  onFilterChange 
}) => {
  const filters: ConversationFilter[] = ['All', 'Today', 'Last 7 Days', 'Last 30 Days'];

  return (
    <div className="p-4 border-b border-gray-200 bg-white">
      <div className="relative mb-4">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-4 w-4 text-gray-400" />
        </div>
        <input
          type="text"
          placeholder="Search conversations..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-gray-50 placeholder-gray-500 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-colors"
        />
      </div>
      
      <div className="flex space-x-2 overflow-x-auto pb-1 scrollbar-hide">
        {filters.map(filter => (
          <button
            key={filter}
            onClick={() => onFilterChange(filter)}
            className={`whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
              activeFilter === filter
                ? 'bg-blue-100 text-blue-700 border border-blue-200'
                : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            {filter}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ConversationFilters;
