import { ChatRequest, ChatResponse } from '../types/chat.types';

export class ChatService {
  private static getApiUrl(): string {
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  static async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.getApiUrl()}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      return await response.json();
    } catch (error) {
      console.error('Chat API Error:', error);
      throw error;
    }
  }
}
