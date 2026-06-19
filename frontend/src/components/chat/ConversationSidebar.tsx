import React from 'react';
import { MessageSquare, Plus, X } from 'lucide-react';
import type { Conversation } from '../../types/chat';

interface ConversationSidebarProps {
  conversations: Conversation[];
  currentId: string | null;
  onSelect: (id: string) => void;
  onNew: () => void;
  isOpen: boolean;
  onClose: () => void;
}

const ConversationSidebar: React.FC<ConversationSidebarProps> = ({
  conversations,
  currentId,
  onSelect,
  onNew,
  isOpen,
  onClose,
}) => {
  // Group conversations by date (simplified)
  const today = new Date().toDateString();
  const yesterday = new Date(Date.now() - 86400000).toDateString();

  const grouped = conversations.reduce((acc, conv) => {
    const date = new Date(conv.updatedAt).toDateString();
    if (date === today) {
      acc.today.push(conv);
    } else if (date === yesterday) {
      acc.yesterday.push(conv);
    } else {
      acc.previous.push(conv);
    }
    return acc;
  }, { today: [] as Conversation[], yesterday: [] as Conversation[], previous: [] as Conversation[] });

  const renderGroup = (title: string, list: Conversation[]) => {
    if (list.length === 0) return null;
    return (
      <div className="mb-6">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 px-3">{title}</h3>
        <div className="space-y-1">
          {list.map((conv) => (
            <button
              key={conv.id}
              onClick={() => onSelect(conv.id)}
              className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 transition-colors group ${
                currentId === conv.id
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              <MessageSquare className={`w-4 h-4 flex-shrink-0 ${currentId === conv.id ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'}`} />
              <span className="truncate text-sm">{conv.title || 'New Conversation'}</span>
            </button>
          ))}
        </div>
      </div>
    );
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/20 z-20 md:hidden transition-opacity"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-30 w-72 bg-gray-50/50 backdrop-blur-xl border-r border-gray-200 transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0 flex flex-col ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        
        {/* Header */}
        <div className="p-4 flex items-center justify-between">
          <button
            onClick={onNew}
            className="flex-1 flex items-center justify-center gap-2 bg-white border border-gray-200 text-gray-700 px-4 py-2.5 rounded-xl hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50/50 hover:shadow-sm transition-all font-medium text-sm"
          >
            <Plus className="w-4 h-4" />
            New Chat
          </button>
          <button onClick={onClose} className="md:hidden ml-2 p-2 text-gray-500 hover:bg-gray-200 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Conversation List */}
        <div className="flex-1 overflow-y-auto px-2 py-2">
          {conversations.length === 0 ? (
            <div className="text-center p-4 text-gray-500 text-sm mt-10">
              No previous conversations
            </div>
          ) : (
            <>
              {renderGroup('Today', grouped.today)}
              {renderGroup('Yesterday', grouped.yesterday)}
              {renderGroup('Previous', grouped.previous)}
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default ConversationSidebar;
