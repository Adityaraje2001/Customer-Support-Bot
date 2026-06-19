export interface TicketResponse {
  id: number;
  session_id: string;
  question: string;
  status: 'open' | 'resolved' | 'closed' | 'in_progress';
}

export interface UpdateTicketStatusRequest {
  status: 'open' | 'resolved' | 'closed' | 'in_progress';
}
