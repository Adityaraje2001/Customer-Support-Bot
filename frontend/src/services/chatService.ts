import authApi from '../api/authApi';
import type { ChatRequest, ChatResponse } from '../types/chat';

export const chatService = {
  sendMessage: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await authApi.post<ChatResponse>('/chat', data);
    return response.data;
  },
};
