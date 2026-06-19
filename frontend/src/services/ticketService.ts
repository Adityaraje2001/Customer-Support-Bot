import authApi from '../api/authApi';
import type { TicketResponse, UpdateTicketStatusRequest } from '../types/ticket';

export const ticketService = {
  getMyTickets: async (): Promise<TicketResponse[]> => {
    const response = await authApi.get<TicketResponse[]>('/tickets/my');
    return response.data;
  },

  getAllTickets: async (): Promise<TicketResponse[]> => {
    const response = await authApi.get<TicketResponse[]>('/tickets/');
    return response.data;
  },

  getTicket: async (ticketId: number): Promise<TicketResponse> => {
    const response = await authApi.get<TicketResponse>(`/tickets/${ticketId}`);
    return response.data;
  },

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
  },

  resolveTicket: async (ticketId: number): Promise<TicketResponse> => {
    const response = await authApi.patch<TicketResponse>(`/tickets/${ticketId}/resolve`);
    return response.data;
  },

  closeTicket: async (ticketId: number): Promise<TicketResponse> => {
    const response = await authApi.patch<TicketResponse>(`/tickets/${ticketId}/close`);
    return response.data;
  },

  markInProgress: async (ticketId: number): Promise<TicketResponse> => {
    const response = await authApi.patch<TicketResponse>(`/tickets/${ticketId}/in-progress`);
    return response.data;
  }
};
