import authApi from "../api/authApi";
import type { Conversation } from "../types/conversation";
import type { Message } from "../types/chat";

export const conversationService = {
  getConversations: async (): Promise<Conversation[]> => {
    const response = await authApi.get<Conversation[]>("/conversations");
    return response.data;
  },

  getConversationMessages: async (
    conversationId: string,
  ): Promise<Message[]> => {
    const response = await authApi.get<Message[]>(
      `/conversations/${conversationId}/messages`,
    );
    return response.data;
  },

  deleteConversation: async (conversationId: string): Promise<void> => {
    await authApi.delete(`/conversations/${conversationId}`);
  },
};
