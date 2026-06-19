import React, { useState } from 'react';
import { CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react';
import type { TicketResponse } from '../../types/ticket';
import { ticketService } from '../../services/ticketService';

interface AdminTicketActionsProps {
  ticket: TicketResponse;
  onUpdate: (updatedTicket: TicketResponse) => void;
}

const AdminTicketActions: React.FC<AdminTicketActionsProps> = ({ ticket, onUpdate }) => {
  const [isLoading, setIsLoading] = useState(false);
  const normalizedStatus = ticket.status.toLowerCase();

  const handleAction = async (action: 'resolve' | 'close' | 'in_progress') => {
    setIsLoading(true);
    try {
      let updatedTicket;
      if (action === 'resolve') {
        updatedTicket = await ticketService.resolveTicket(ticket.id);
      } else if (action === 'close') {
        updatedTicket = await ticketService.closeTicket(ticket.id);
      } else {
        updatedTicket = await ticketService.markInProgress(ticket.id);
      }
      onUpdate(updatedTicket);
    } catch (error) {
      console.error('Failed to update ticket status', error);
      // Let the parent or a global interceptor handle the toast error notification
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center gap-2">
      {isLoading ? (
        <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
      ) : (
        <>
          {normalizedStatus !== 'in_progress' && normalizedStatus !== 'resolved' && normalizedStatus !== 'closed' && (
            <button 
              onClick={() => handleAction('in_progress')}
              className="p-1.5 text-amber-600 hover:bg-amber-50 rounded-md transition-colors"
              title="Mark In Progress"
            >
              <Clock className="w-4 h-4" />
            </button>
          )}
          
          {normalizedStatus !== 'resolved' && normalizedStatus !== 'closed' && (
            <button 
              onClick={() => handleAction('resolve')}
              className="p-1.5 text-emerald-600 hover:bg-emerald-50 rounded-md transition-colors"
              title="Resolve Ticket"
            >
              <CheckCircle className="w-4 h-4" />
            </button>
          )}
          
          {normalizedStatus !== 'closed' && (
            <button 
              onClick={() => handleAction('close')}
              className="p-1.5 text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
              title="Close Ticket"
            >
              <XCircle className="w-4 h-4" />
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default AdminTicketActions;
