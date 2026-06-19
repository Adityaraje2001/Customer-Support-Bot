export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  agent_used?: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  agentUsed?: string;
}

export interface Conversation {
  id: string;
  title: string;
  updatedAt: string;
  messages: Message[];
}
