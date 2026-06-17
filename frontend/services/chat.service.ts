import { ChatRequest, ChatResponse } from '../types/chat.types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Send a chat message to the backend and return the full response.
 *
 * @param message    - The user's message text
 * @param sessionId  - Optional session ID for conversation continuity;
 *                     omit on the first message to let the backend create one.
 * @returns The assistant's response text and the session ID to reuse.
 */
export async function sendMessage(
  message: string,
  sessionId?: string
): Promise<ChatResponse> {
  const payload: ChatRequest = {
    message,
    session_id: sessionId,
  };

  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text().catch(() => '');
    throw new Error(
      `Chat request failed (${response.status}): ${errorBody || response.statusText}`
    );
  }

  const data: ChatResponse = await response.json();
  return data;
}
