import React from 'react';
import { MessageSquareOff } from 'lucide-react';

const ConversationEmptyState: React.FC = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-gray-50 rounded-2xl border border-dashed border-gray-300 mx-4 my-auto h-full min-h-[400px]">
      <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4 text-gray-400">
        <MessageSquareOff className="w-8 h-8" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">No conversation selected</h3>
      <p className="text-gray-500 max-w-sm">
        Select a conversation from the list to view its history, or start a new chat to get help.
      </p>
    </div>
  );
};

export default ConversationEmptyState;
