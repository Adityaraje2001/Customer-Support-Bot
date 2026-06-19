import React from 'react';
import { Bot } from 'lucide-react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-4 max-w-[85%] mr-auto animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-blue-600 shadow-md flex items-center justify-center">
        <Bot className="w-4 h-4 text-white" />
      </div>
      <div className="px-5 py-4 rounded-2xl bg-white shadow-sm border border-gray-100 rounded-tl-sm flex items-center gap-2">
        <div className="flex gap-1.5 items-center h-4">
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 rounded-full bg-blue-600 animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
