export type TicketStatus = 'open' | 'resolved' | 'closed' | 'in_progress' | 'OPEN' | 'RESOLVED' | 'CLOSED' | 'IN_PROGRESS';

export interface TicketResponse {
  id: number;
  session_id: string;
  question: string;
  status: TicketStatus;
  created_at?: string;
}

export interface UpdateTicketStatusRequest {
  status: TicketStatus;
}
