import React from 'react';
import { Bot } from 'lucide-react';
import SuggestedPrompts from './SuggestedPrompts';

interface EmptyStateProps {
  onSelectPrompt: (prompt: string) => void;
}

const EmptyState: React.FC<EmptyStateProps> = ({ onSelectPrompt }) => {
  return (
    <div className="flex flex-col items-center justify-center h-full px-4 animate-in fade-in duration-500">
      <div className="w-16 h-16 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl flex items-center justify-center mb-6 shadow-sm border border-blue-100">
        <Bot className="w-8 h-8 text-blue-600" />
      </div>
      
      <h2 className="text-2xl font-bold text-gray-900 mb-2">How can I help you today?</h2>
      <p className="text-gray-500 text-center max-w-md mb-8">
        I'm your AI support assistant. You can ask me about billing, your account, or create and check on support tickets.
      </p>

      <SuggestedPrompts onSelect={onSelectPrompt} />
    </div>
  );
};

export default EmptyState;
