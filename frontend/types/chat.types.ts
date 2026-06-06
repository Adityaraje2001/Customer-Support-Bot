export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  createdAt: Date;
}

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
}
