import authApi from '../api/authApi';
import type { TicketResponse, UpdateTicketStatusRequest } from '../types/ticket';

export const ticketService = {
  getOpenTickets: async (): Promise<TicketResponse[]> => {
    const response = await authApi.get<TicketResponse[]>('/tickets/open');
    return response.data;
  },

  getResolvedTickets: async (): Promise<TicketResponse[]> => {
    const response = await authApi.get<TicketResponse[]>('/tickets/resolved');
    return response.data;
  },

  updateTicketStatus: async (ticketId: number, request: UpdateTicketStatusRequest): Promise<TicketResponse> => {
    const response = await authApi.patch<TicketResponse>(`/tickets/${ticketId}`, request);
    return response.data;
  }
};
