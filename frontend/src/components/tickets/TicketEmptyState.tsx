import React from 'react';
import { Ticket } from 'lucide-react';

interface TicketEmptyStateProps {
  message?: string;
  subMessage?: string;
}

const TicketEmptyState: React.FC<TicketEmptyStateProps> = ({ 
  message = "No tickets found", 
  subMessage = "We couldn't find any tickets matching your criteria." 
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 bg-white rounded-xl border border-gray-200 shadow-sm text-center">
      <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
        <Ticket className="w-8 h-8 text-gray-400" />
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-1">{message}</h3>
      <p className="text-sm text-gray-500 max-w-sm">{subMessage}</p>
    </div>
  );
};

export default TicketEmptyState;
