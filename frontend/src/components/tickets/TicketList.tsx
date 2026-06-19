import React from 'react';
import type { TicketResponse } from '../../types/ticket';
import TicketCard from './TicketCard';
import TicketEmptyState from './TicketEmptyState';

interface TicketListProps {
  tickets: TicketResponse[];
  isLoading: boolean;
  onTicketClick: (ticket: TicketResponse) => void;
  emptyMessage?: string;
  emptySubMessage?: string;
}

const TicketList: React.FC<TicketListProps> = ({ 
  tickets, 
  isLoading, 
  onTicketClick,
  emptyMessage,
  emptySubMessage
}) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 animate-pulse">
            <div className="flex justify-between items-start mb-4">
              <div className="h-6 w-20 bg-gray-200 rounded-md"></div>
              <div className="h-4 w-24 bg-gray-100 rounded"></div>
            </div>
            <div className="space-y-2 mt-4">
              <div className="h-4 w-full bg-gray-200 rounded"></div>
              <div className="h-4 w-4/5 bg-gray-200 rounded"></div>
            </div>
            <div className="mt-6 flex justify-between items-center">
              <div className="h-6 w-24 bg-gray-100 rounded"></div>
              <div className="h-4 w-16 bg-gray-200 rounded"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (tickets.length === 0) {
    return <TicketEmptyState message={emptyMessage} subMessage={emptySubMessage} />;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {tickets.map((ticket) => (
        <TicketCard 
          key={ticket.id} 
          ticket={ticket} 
          onClick={onTicketClick} 
        />
      ))}
    </div>
  );
};

export default TicketList;
