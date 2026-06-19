import React from 'react';
import type { TicketResponse } from '../../types/ticket';
import TicketStatusBadge from './TicketStatusBadge';
import { X, Calendar, Fingerprint, HelpCircle } from 'lucide-react';

interface TicketDetailsModalProps {
  ticket: TicketResponse;
  isOpen: boolean;
  onClose: () => void;
}

const TicketDetailsModal: React.FC<TicketDetailsModalProps> = ({ ticket, isOpen, onClose }) => {
  if (!isOpen) return null;

  const displayDate = ticket.created_at 
    ? new Date(ticket.created_at).toLocaleString() 
    : 'N/A';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        <div className="flex justify-between items-center p-6 border-b border-gray-100">
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-semibold text-gray-900">Ticket Details</h2>
            <span className="text-sm font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-md">
              #{ticket.id}
            </span>
          </div>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 hover:bg-gray-100 p-2 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 mb-1">Current Status</p>
              <TicketStatusBadge status={ticket.status} />
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500 mb-1">Created Date</p>
              <div className="flex items-center text-gray-900 font-medium gap-1.5 justify-end">
                <Calendar className="w-4 h-4 text-gray-400" />
                {displayDate}
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
            <h3 className="text-sm font-medium text-gray-500 flex items-center gap-2 mb-3">
              <HelpCircle className="w-4 h-4" />
              Customer Question
            </h3>
            <p className="text-gray-900 leading-relaxed">
              {ticket.question}
            </p>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-500 flex items-center gap-2 mb-2">
              <Fingerprint className="w-4 h-4" />
              Technical Details
            </h3>
            <div className="bg-gray-50 rounded-lg p-3 border border-gray-100 font-mono text-xs text-gray-600 break-all">
              <span className="font-semibold text-gray-400 mr-2">Session ID:</span> 
              {ticket.session_id}
            </div>
          </div>
        </div>

        <div className="bg-gray-50 px-6 py-4 border-t border-gray-100 flex justify-end">
          <button 
            onClick={onClose}
            className="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg font-medium shadow-sm hover:bg-gray-50 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default TicketDetailsModal;
