import React from 'react';
import type { TicketResponse } from '../../types/ticket';
import TicketStatusBadge from './TicketStatusBadge';
import { ChevronRight, Calendar, MessageSquare } from 'lucide-react';

interface TicketCardProps {
  ticket: TicketResponse;
  onClick: (ticket: TicketResponse) => void;
}

const TicketCard: React.FC<TicketCardProps> = ({ ticket, onClick }) => {
  const displayDate = ticket.created_at 
    ? new Date(ticket.created_at).toLocaleDateString() 
    : 'N/A';

  return (
    <div 
      onClick={() => onClick(ticket)}
      className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer overflow-hidden group"
    >
      <div className="p-5">
        <div className="flex justify-between items-start mb-3">
          <div className="flex items-center gap-3">
            <span className="text-sm font-semibold text-gray-500 bg-gray-100 px-2 py-1 rounded-md">
              #{ticket.id}
            </span>
            <TicketStatusBadge status={ticket.status} />
          </div>
          <div className="flex items-center text-gray-400 text-sm gap-1.5">
            <Calendar className="w-4 h-4" />
            {displayDate}
          </div>
        </div>
        
        <div className="mt-2">
          <h3 className="text-gray-900 font-medium line-clamp-2 text-base flex gap-2 items-start">
            <MessageSquare className="w-5 h-5 text-indigo-500 shrink-0 mt-0.5" />
            {ticket.question}
          </h3>
        </div>
      </div>
      
      <div className="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between items-center group-hover:bg-indigo-50 transition-colors duration-200">
        <span className="text-xs text-gray-500 font-mono bg-white px-2 py-1 rounded border border-gray-200 shadow-sm">
          Session: {ticket.session_id.substring(0, 8)}...
        </span>
        <button className="text-indigo-600 text-sm font-medium flex items-center gap-1 group-hover:text-indigo-700">
          View Details
          <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};

export default TicketCard;
