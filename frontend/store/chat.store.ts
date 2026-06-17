import { useState, useCallback } from 'react';
import { Message } from '../types/chat.types';
import { sendMessage } from '../services/chat.service';

/**
 * Custom React hook that manages chat state:
 * - Message history
 * - Session ID (assigned by the backend on the first response)
 * - Loading / error states
 *
 * Session flow:
 *   1. First message → session_id is undefined → backend creates one
 *   2. Backend returns session_id in the response
 *   3. Hook stores it and reuses it for all subsequent messages
 */
export function useChatStore() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = useCallback(
    async (userInput: string) => {
      if (!userInput.trim() || isLoading) return;

      // Add the user message to the UI immediately
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: userInput.trim(),
        createdAt: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        const data = await sendMessage(userInput.trim(), sessionId);

        // Store the session_id returned by the backend
        if (data.session_id) {
          setSessionId(data.session_id);
        }

        // Add the assistant response
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.response,
          createdAt: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        console.error('Chat error:', err);
        setError('Something went wrong. Please try again.');
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, sessionId]
  );

  return { messages, isLoading, error, send };
}
