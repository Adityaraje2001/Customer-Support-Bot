import type { Message } from './chat';

export interface Conversation {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  messageCount: number;
  messages?: Message[];
}

export type ConversationFilter = 'Today' | 'Last 7 Days' | 'Last 30 Days' | 'All';
