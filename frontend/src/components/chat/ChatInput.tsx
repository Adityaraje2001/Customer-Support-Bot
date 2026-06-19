import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || isLoading) return;

    onSendMessage(input.trim());
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="p-4 bg-white/80 backdrop-blur-md border-t border-gray-100">
      <div className="max-w-4xl mx-auto relative">
        <form
          onSubmit={handleSubmit}
          className="relative flex items-end bg-white border border-gray-200 rounded-2xl shadow-sm focus-within:ring-2 focus-within:ring-blue-500/20 focus-within:border-blue-500 transition-all overflow-hidden"
        >
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message SupportBot..."
            disabled={isLoading}
            rows={1}
            className="w-full max-h-[200px] resize-none pl-4 pr-12 py-3.5 bg-transparent border-none focus:outline-none focus:ring-0 text-gray-700 placeholder-gray-400 disabled:opacity-50"
            style={{ minHeight: '52px' }}
          />
          <div className="absolute right-2 bottom-2">
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className={`p-2 rounded-xl transition-all duration-200 ${
                !input.trim() || isLoading
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-md active:scale-95'
              }`}
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4 ml-0.5" />
              )}
            </button>
          </div>
        </form>
        <div className="mt-2 text-center">
          <p className="text-[11px] text-gray-400">
            SupportBot can make mistakes. Consider verifying important information.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
