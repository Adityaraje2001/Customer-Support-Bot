export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  createdAt: Date;
  /** True while the assistant message is still being streamed in */
  isStreaming?: boolean;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  session_id?: string;
}

/**
 * Callback invoked each time a new chunk of text arrives from the
 * streaming endpoint. The component uses this to append tokens to
 * the assistant message in real time.
 */
export type StreamChunkCallback = (chunk: string) => void;

