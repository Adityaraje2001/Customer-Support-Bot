import React from 'react';
import type { TicketStatus } from '../../types/ticket';
import { CheckCircle2, Clock, XCircle, AlertCircle } from 'lucide-react';

interface TicketStatusBadgeProps {
  status: TicketStatus;
  className?: string;
}

const TicketStatusBadge: React.FC<TicketStatusBadgeProps> = ({ status, className = '' }) => {
  const normalizedStatus = status.toLowerCase();

  switch (normalizedStatus) {
    case 'open':
      return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200 ${className}`}>
          <AlertCircle className="w-3.5 h-3.5" />
          Open
        </span>
      );
    case 'in_progress':
      return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-800 border border-amber-200 ${className}`}>
          <Clock className="w-3.5 h-3.5" />
          In Progress
        </span>
      );
    case 'resolved':
      return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200 ${className}`}>
          <CheckCircle2 className="w-3.5 h-3.5" />
          Resolved
        </span>
      );
    case 'closed':
      return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-200 ${className}`}>
          <XCircle className="w-3.5 h-3.5" />
          Closed
        </span>
      );
    default:
      return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-200 ${className}`}>
          {status}
        </span>
      );
  }
};

export default TicketStatusBadge;
