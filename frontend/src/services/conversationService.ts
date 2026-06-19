import type { Conversation } from '../types/conversation';
import type { Message } from '../types/chat';

// Mock data to simulate backend response
let mockConversations: Conversation[] = [
  {
    id: 'conv-1',
    title: 'Refund Policy Questions',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 day ago
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    messageCount: 4,
    messages: [
      { id: 'm-1', role: 'user', content: 'What is your refund policy?', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString() },
      { id: 'm-2', role: 'assistant', content: 'Our refund policy allows returns within 30 days of purchase.', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 + 1000 * 60).toISOString(), agentUsed: 'Customer Support' },
      { id: 'm-3', role: 'user', content: 'Does that apply to sale items?', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 + 1000 * 60 * 2).toISOString() },
      { id: 'm-4', role: 'assistant', content: 'Sale items are final sale and cannot be refunded.', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 + 1000 * 60 * 3).toISOString(), agentUsed: 'Customer Support' }
    ]
  },
  {
    id: 'conv-2',
    title: 'Technical Issue with Login',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 10).toISOString(), // 10 days ago
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 10).toISOString(),
    messageCount: 2,
    messages: [
      { id: 'm-5', role: 'user', content: 'I cannot log in to my account.', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 10).toISOString() },
      { id: 'm-6', role: 'assistant', content: 'I am sorry to hear that. Have you tried resetting your password?', timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 10 + 1000 * 30).toISOString(), agentUsed: 'Technical Support' }
    ]
  }
];

export const conversationService = {
  getConversations: async (): Promise<Conversation[]> => {
    // Simulating API latency
    return new Promise((resolve) => {
      setTimeout(() => {
        // Return without messages array to simulate list view
        resolve(mockConversations.map(({ messages, ...rest }) => rest));
      }, 600);
    });
  },

  getConversationMessages: async (conversationId: string): Promise<Message[]> => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const conv = mockConversations.find(c => c.id === conversationId);
        if (conv && conv.messages) {
          resolve(conv.messages);
        } else {
          reject(new Error('Conversation not found'));
        }
      }, 400);
    });
  },

  deleteConversation: async (conversationId: string): Promise<void> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        mockConversations = mockConversations.filter(c => c.id !== conversationId);
        resolve();
      }, 500);
    });
  }
};
