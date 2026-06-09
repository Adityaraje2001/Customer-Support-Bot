import { ChatRequest, ChatResponse, StreamChunkCallback } from '../types/chat.types';

export class ChatService {
  private static getApiUrl(): string {
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  // ──────────────────────────────────────────────
  // Non-streaming: sends a message and waits for the full response
  // ──────────────────────────────────────────────
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

  // ──────────────────────────────────────────────
  // Streaming: reads tokens one-by-one from the SSE stream
  // ──────────────────────────────────────────────
  /**
   * Send a message and stream the response token-by-token.
   *
   * @param request  - The chat request payload (same as non-streaming)
   * @param onChunk  - Called with each token as it arrives from the backend
   *
   * How it works:
   * 1. We POST to /api/chat/stream which returns a text/event-stream.
   * 2. We grab a ReadableStream reader from the response body.
   * 3. We decode each chunk of bytes into text and parse SSE lines.
   * 4. For each "data: <token>" line, we call onChunk(token).
   * 5. When we see "data: [DONE]", we stop reading.
   */
  static async sendMessageStream(
    request: ChatRequest,
    onChunk: StreamChunkCallback
  ): Promise<void> {
    // Start the streaming request
    const response = await fetch(`${this.getApiUrl()}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    // Handle HTTP-level errors (e.g. 500 from the backend)
    if (!response.ok) {
      throw new Error(`Stream request failed with status ${response.status}`);
    }

    // response.body is a ReadableStream of Uint8Array chunks.
    // If the browser doesn't support streaming (very rare), bail out.
    if (!response.body) {
      throw new Error('ReadableStream not supported in this browser');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    // Buffer for incomplete SSE lines that may be split across chunks.
    // Network chunks don't always align with SSE event boundaries,
    // so we accumulate text and process complete lines.
    let buffer = '';

    try {
      while (true) {
        // Read the next chunk of bytes from the stream
        const { done, value } = await reader.read();

        // The stream has been fully consumed
        if (done) break;

        // Decode the binary chunk into a string and add to our buffer
        buffer += decoder.decode(value, { stream: true });

        // Split the buffer into individual lines.
        // SSE format uses "\n\n" to separate events, but we process
        // line-by-line looking for "data: " prefixed lines.
        const lines = buffer.split('\n');

        // The last element might be an incomplete line — keep it in the
        // buffer for the next iteration. Complete lines end with \n so
        // the last element after split is either '' or a partial line.
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmedLine = line.trim();

          // Skip empty lines (SSE event separators)
          if (!trimmedLine) continue;

          // Each SSE data line starts with "data: "
          if (trimmedLine.startsWith('data: ')) {
            const data = trimmedLine.slice(6); // Remove "data: " prefix

            // [DONE] signals the stream is complete
            if (data === '[DONE]') {
              return;
            }

            // [ERROR] signals a backend error during streaming
            if (data.startsWith('[ERROR]')) {
              throw new Error(data.slice(8)); // Remove "[ERROR] " prefix
            }

            // It's a normal token — pass it to the UI callback
            onChunk(data);
          }
        }
      }
    } finally {
      // Always release the reader lock, even if we exit early due to
      // [DONE] or an error. This prevents resource leaks.
      reader.releaseLock();
    }
  }
}
