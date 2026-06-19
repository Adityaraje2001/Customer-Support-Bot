import React, { useState, useRef, useEffect, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ConversationSidebar from './ConversationSidebar';
import ChatHeader from './ChatHeader';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import EmptyState from './EmptyState';
import TypingIndicator from './TypingIndicator';
import { chatService } from '../../services/chatService';
import type { Message, Conversation } from '../../types/chat';

const ChatContainer: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversations from local storage
  useEffect(() => {
    const saved = localStorage.getItem('chat_sessions');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setConversations(parsed);
        if (parsed.length > 0) {
          setCurrentId(parsed[0].id);
        }
      } catch (e) {
        console.error('Failed to parse conversations', e);
      }
    }
  }, []);

  // Save to local storage on change
  useEffect(() => {
    localStorage.setItem('chat_sessions', JSON.stringify(conversations));
  }, [conversations]);

  // Online status listener
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const currentConversation = conversations.find(c => c.id === currentId);
  const messages = currentConversation?.messages || [];

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  const handleNewChat = () => {
    setCurrentId(null);
    if (window.innerWidth < 768) setIsSidebarOpen(false);
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    let targetConvId = currentId;

    // Create a new conversation if none selected or empty
    if (!targetConvId) {
      const newConv: Conversation = {
        id: uuidv4(), // We use uuid for UI, actual session id comes from backend
        title: content.substring(0, 30) + (content.length > 30 ? '...' : ''),
        updatedAt: new Date().toISOString(),
        messages: [],
      };
      setConversations(prev => [newConv, ...prev]);
      setCurrentId(newConv.id);
      targetConvId = newConv.id;
    }

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setConversations(prev => {
      return prev.map(c => {
        if (c.id === targetConvId) {
          return {
            ...c,
            updatedAt: new Date().toISOString(),
            messages: [...c.messages, userMessage],
          };
        }
        return c;
      });
    });

    setIsLoading(true);

    // Initial placeholder for assistant message
    const botMessageId = uuidv4();
    const placeholderMsg: Message = {
      id: botMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
    };

    let assistantHasStarted = false;

    try {
      // We pass targetConvId. The backend expects a string.
      
      const generator = chatService.streamChat({
        message: content,
        session_id: targetConvId, // Re-use the UI ID as session ID for simplicity
      });

      for await (const chunk of generator) {
        if (!assistantHasStarted) {
          assistantHasStarted = true;
          setConversations(prev => prev.map(c => {
            if (c.id === targetConvId) {
              return { ...c, messages: [...c.messages, placeholderMsg] };
            }
            return c;
          }));
        }

        // Try to parse SSE chunks if backend sends SSE, or just raw text.
        // Assuming raw text stream chunks here:
        setConversations(prev => prev.map(c => {
          if (c.id === targetConvId) {
            const msgs = [...c.messages];
            const lastIdx = msgs.length - 1;
            if (msgs[lastIdx].id === botMessageId) {
              msgs[lastIdx] = { ...msgs[lastIdx], content: msgs[lastIdx].content + chunk };
            }
            return { ...c, messages: msgs };
          }
          return c;
        }));
        scrollToBottom();
      }

    } catch (error) {
      console.error('Streaming error:', error);
      // Fallback or error message
      if (!assistantHasStarted) {
        setConversations(prev => prev.map(c => {
          if (c.id === targetConvId) {
            return {
              ...c,
              messages: [...c.messages, {
                id: botMessageId,
                role: 'assistant',
                content: 'Sorry, I encountered an error connecting to the server. Please try again.',
                timestamp: new Date().toISOString(),
              }]
            };
          }
          return c;
        }));
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] w-full overflow-hidden bg-white">
      <ConversationSidebar
        conversations={conversations}
        currentId={currentId}
        onSelect={(id) => {
          setCurrentId(id);
          if (window.innerWidth < 768) setIsSidebarOpen(false);
        }}
        onNew={handleNewChat}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />

      <div className="flex-1 flex flex-col min-w-0 relative bg-white">
        <ChatHeader
          sessionId={currentId || undefined}
          isOnline={isOnline}
          onMenuClick={() => setIsSidebarOpen(true)}
        />

        <div className="flex-1 overflow-y-auto bg-gray-50/30">
          <div className="max-w-4xl mx-auto p-4 sm:p-6 w-full h-full flex flex-col">
            {messages.length === 0 ? (
              <EmptyState onSelectPrompt={handleSendMessage} />
            ) : (
              <div className="space-y-6 pb-4">
                {messages.map(msg => (
                  <ChatMessage key={msg.id} message={msg} />
                ))}
                
                {isLoading && (
                  <div className="mt-4">
                    <TypingIndicator />
                  </div>
                )}
                <div ref={messagesEndRef} className="h-1" />
              </div>
            )}
          </div>
        </div>

        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default ChatContainer;
