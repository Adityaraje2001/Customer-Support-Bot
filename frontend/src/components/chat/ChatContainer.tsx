import React, { useState, useRef, useEffect, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import toast from 'react-hot-toast';
import ConversationSidebar from './ConversationSidebar';
import ChatHeader from './ChatHeader';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import EmptyState from './EmptyState';
import TypingIndicator from './TypingIndicator';
import { chatService } from '../../services/chatService';
import { feedbackService } from '../../services/feedbackService';
import type { Message, Conversation } from '../../types/chat';
import type { FeedbackCreate } from '../../types/feedback';

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

  const handleFeedback = async (
    messageId: string,
    feedbackType: 'helpful' | 'not_helpful',
    comment?: string,
  ) => {
    // Find the assistant message
    const conversation = conversations.find(c => c.id === currentId);
    if (!conversation) return;

    const targetMsg = conversation.messages.find(m => m.id === messageId);
    if (!targetMsg || targetMsg.role !== 'assistant') return;

    // Find the user message that precedes this assistant message
    const msgIndex = conversation.messages.indexOf(targetMsg);
    const userMsg = conversation.messages
      .slice(0, msgIndex)
      .reverse()
      .find(m => m.role === 'user');

    const feedbackData: FeedbackCreate = {
      session_id: targetMsg.sessionId || currentId || '',
      message_id: targetMsg.messageId || targetMsg.id,
      question: userMsg?.content || '',
      answer: targetMsg.content,
      route_selected: targetMsg.agentUsed,
      feedback_type: feedbackType,
      feedback_comment: comment || undefined,
    };

    try {
      await feedbackService.submitFeedback(feedbackData);

      // Mark as given in local state
      setConversations(prev =>
        prev.map(c => {
          if (c.id !== currentId) return c;
          return {
            ...c,
            messages: c.messages.map(m =>
              m.id === messageId ? { ...m, feedbackGiven: feedbackType } : m,
            ),
          };
        }),
      );

      toast.success('Thank you for your feedback!', {
        duration: 3000,
        style: {
          borderRadius: '12px',
          background: '#1f2937',
          color: '#fff',
          fontSize: '14px',
        },
      });
    } catch (error: any) {
      if (error?.response?.status === 409) {
        toast.error('Feedback already submitted for this message.', {
          duration: 3000,
          style: {
            borderRadius: '12px',
            background: '#1f2937',
            color: '#fff',
            fontSize: '14px',
          },
        });
        // Mark as given anyway so buttons disable
        setConversations(prev =>
          prev.map(c => {
            if (c.id !== currentId) return c;
            return {
              ...c,
              messages: c.messages.map(m =>
                m.id === messageId ? { ...m, feedbackGiven: feedbackType } : m,
              ),
            };
          }),
        );
      } else {
        toast.error('Failed to submit feedback. Please try again.', {
          duration: 3000,
          style: {
            borderRadius: '12px',
            background: '#1f2937',
            color: '#fff',
            fontSize: '14px',
          },
        });
      }
    }
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

    const botMessageId = uuidv4();

    try {
      // Use the non-streaming endpoint which runs the full LangGraph workflow
      // (router → ticket/support/billing/escalation agents)
      const response = await chatService.sendMessage({
        message: content,
        session_id: targetConvId, // Re-use the UI ID as session ID for simplicity
      });

      const botMessage: Message = {
        id: botMessageId,
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        agentUsed: response.agent_used,
        messageId: response.message_id || botMessageId,
        sessionId: response.session_id || targetConvId,
        feedbackGiven: null,
      };

      setConversations(prev => prev.map(c => {
        if (c.id === targetConvId) {
          return { ...c, messages: [...c.messages, botMessage] };
        }
        return c;
      }));
      scrollToBottom();

    } catch (error) {
      console.error('Chat error:', error);
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
                  <ChatMessage
                    key={msg.id}
                    message={msg}
                    onFeedback={handleFeedback}
                  />
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
