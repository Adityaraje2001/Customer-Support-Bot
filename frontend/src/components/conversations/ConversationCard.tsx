import React from 'react';
import type { Conversation } from '../../types/conversation';
import { MessageSquare, Calendar, ChevronRight } from 'lucide-react';

interface ConversationCardProps {
  conversation: Conversation;
  isActive: boolean;
  onClick: () => void;
}

const ConversationCard: React.FC<ConversationCardProps> = ({ conversation, isActive, onClick }) => {
  const formattedDate = new Date(conversation.createdAt).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });

  return (
    <div 
      onClick={onClick}
      className={`p-4 cursor-pointer transition-all border-l-4 ${
        isActive 
          ? 'bg-blue-50 border-blue-600 shadow-sm' 
          : 'bg-white border-transparent hover:bg-gray-50 border-b border-b-gray-100 last:border-b-transparent'
      }`}
    >
      <div className="flex justify-between items-start mb-2">
        <h4 className={`font-semibold text-sm truncate pr-2 ${isActive ? 'text-blue-900' : 'text-gray-900'}`}>
          {conversation.title || 'Untitled Conversation'}
        </h4>
        <ChevronRight className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-blue-600' : 'text-gray-400'}`} />
      </div>
      
      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center gap-1.5">
          <Calendar className="w-3.5 h-3.5" />
          <span>{formattedDate}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <MessageSquare className="w-3.5 h-3.5" />
          <span>{conversation.messageCount} {conversation.messageCount === 1 ? 'msg' : 'msgs'}</span>
        </div>
      </div>
    </div>
  );
};

export default ConversationCard;
