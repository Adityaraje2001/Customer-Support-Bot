'use client';

import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import { Message } from '../types/chat.types';
import { ChatService } from '../services/chat.service';

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // Generate a stable session_id per component mount so the backend
  // can link all messages in a single conversation together.
  const sessionId = useMemo(() => crypto.randomUUID(), []);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change (including each new token)
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // ── 1. Add the user's message to the chat ──
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue.trim(),
      createdAt: new Date(),
    };

    // Generate a unique ID for the assistant's response message.
    // We create the placeholder now so we can update it as tokens arrive.
    const assistantMessageId = (Date.now() + 1).toString();

    setMessages((prev) => [
      ...prev,
      userMessage,
      // ── 2. Add an empty assistant placeholder with isStreaming=true ──
      // This shows up immediately in the chat with a blinking cursor,
      // giving the user instant visual feedback that a response is coming.
      {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        createdAt: new Date(),
        isStreaming: true,
      },
    ]);

    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // ── 3. Start streaming — each token updates the placeholder ──
      await ChatService.sendMessageStream(
        { message: userMessage.content, session_id: sessionId },
        (chunk: string) => {
          // This callback fires for every token the backend sends.
          // We use a functional state update to append the new chunk
          // to the existing content of the assistant message.
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === assistantMessageId
                ? { ...msg, content: msg.content + chunk }
                : msg
            )
          );
        }
      );

      // ── 4. Streaming complete — remove the streaming cursor ──
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId
            ? { ...msg, isStreaming: false }
            : msg
        )
      );
    } catch (err) {
      // ── 5. On error, remove the empty placeholder and show error ──
      setMessages((prev) =>
        prev.filter((msg) => msg.id !== assistantMessageId)
      );
      setError('Something went wrong. Please try again.');
      console.error('Streaming error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto flex flex-col h-[600px] border border-gray-200 rounded-lg shadow-sm bg-white overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h2 className="text-lg font-semibold text-gray-800">Support Chat</h2>
      </div>

      {/* Messages List */}
      <div className="flex-1 p-6 overflow-y-auto bg-gray-50/50">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-gray-400">
            Send a message to start the conversation
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] px-4 py-2 rounded-2xl ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'
                  }`}
                >
                  {/* Message text + optional streaming cursor */}
                  {msg.content}
                  {msg.isStreaming && (
                    <span className="streaming-cursor" aria-hidden="true" />
                  )}
                </div>
              </div>
            ))}
            
            {/* Error Message */}
            {error && (
              <div className="text-center text-red-500 text-sm py-2">
                {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-gray-200">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500 text-black"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

