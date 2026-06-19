import React from 'react';
import type { Conversation } from '../../types/conversation';
import ChatMessage from '../chat/ChatMessage';
import { Trash2 } from 'lucide-react';

interface ConversationViewerProps {
  conversation: Conversation | null;
  loading: boolean;
  onDelete: (id: string) => void;
}

const ConversationViewer: React.FC<ConversationViewerProps> = ({ conversation, loading, onDelete }) => {
  if (loading) {
    return (
      <div className="flex-1 flex flex-col h-full bg-white animate-pulse p-6">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-8"></div>
        <div className="space-y-6">
          <div className="flex gap-4">
            <div className="w-8 h-8 bg-gray-200 rounded-full flex-shrink-0"></div>
            <div className="h-16 bg-gray-200 rounded-2xl w-2/3"></div>
          </div>
          <div className="flex gap-4 flex-row-reverse">
            <div className="w-8 h-8 bg-gray-200 rounded-full flex-shrink-0"></div>
            <div className="h-16 bg-gray-200 rounded-2xl w-2/3"></div>
          </div>
          <div className="flex gap-4">
            <div className="w-8 h-8 bg-gray-200 rounded-full flex-shrink-0"></div>
            <div className="h-16 bg-gray-200 rounded-2xl w-2/3"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!conversation) return null;

  return (
    <div className="flex-1 flex flex-col h-full bg-white relative">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-white sticky top-0 z-10">
        <div>
          <h2 className="text-lg font-bold text-gray-900">{conversation.title || 'Conversation'}</h2>
          <p className="text-sm text-gray-500">
            {new Date(conversation.createdAt).toLocaleDateString()} • {conversation.messageCount} messages
          </p>
        </div>
        <button
          onClick={() => {
            if (window.confirm('Are you sure you want to delete this conversation?')) {
              onDelete(conversation.id);
            }
          }}
          className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors group"
          title="Delete Conversation"
        >
          <Trash2 className="w-5 h-5 group-hover:scale-110 transition-transform" />
        </button>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/50">
        {conversation.messages && conversation.messages.length > 0 ? (
          conversation.messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        ) : (
          <div className="text-center text-gray-500 py-10">
            No messages found in this conversation.
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationViewer;
