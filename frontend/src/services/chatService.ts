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
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split('\n\n');
      buffer = parts.pop() || '';

      for (const part of parts) {
        if (part.startsWith('data: ')) {
          const content = part.slice(6);
          if (content.trim() === '[DONE]') {
            return;
          }
          if (content.trim().startsWith('[ERROR]')) {
            throw new Error(content);
          }
          try {
            const token = JSON.parse(content);
            yield token;
          } catch (e) {
            // Fallback for non-json data or legacy format
            yield content;
          }
        }
      }
    }
  },
};
