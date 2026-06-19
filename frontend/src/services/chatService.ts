import authApi from '../api/authApi';
import type { ChatRequest, ChatResponse } from '../types/chat';
import { getToken } from '../utils/token';

export const chatService = {
  sendMessage: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await authApi.post<ChatResponse>('/chat', data);
    return response.data;
  },

  streamChat: async function* (data: ChatRequest): AsyncGenerator<string, void, unknown> {
    const token = getToken();
    const response = await fetch('http://localhost:8000/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Streaming failed with status: ${response.status}`);
    }

    if (!response.body) {
      throw new Error('ReadableStream not supported');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      yield decoder.decode(value, { stream: true });
    }
  },
};
