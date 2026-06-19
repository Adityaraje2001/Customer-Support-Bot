import React from 'react';
import type { Conversation } from '../../types/conversation';
import ConversationCard from './ConversationCard';

interface ConversationListProps {
  conversations: Conversation[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  loading: boolean;
}

const ConversationList: React.FC<ConversationListProps> = ({ conversations, selectedId, onSelect, loading }) => {
  if (loading) {
    return (
      <div className="divide-y divide-gray-100">
        {[1, 2, 3, 4, 5].map(i => (
          <div key={i} className="p-4 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
            <div className="flex justify-between">
              <div className="h-3 bg-gray-200 rounded w-1/3"></div>
              <div className="h-3 bg-gray-200 rounded w-1/4"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      {conversations.map(conversation => (
        <ConversationCard
          key={conversation.id}
          conversation={conversation}
          isActive={selectedId === conversation.id}
          onClick={() => onSelect(conversation.id)}
        />
      ))}
    </div>
  );
};

export default ConversationList;
