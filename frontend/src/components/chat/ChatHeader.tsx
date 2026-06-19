import React from 'react';
import { Bot, Wifi, WifiOff, Menu } from 'lucide-react';

interface ChatHeaderProps {
  sessionId?: string;
  isOnline: boolean;
  onMenuClick: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ sessionId, isOnline, onMenuClick }) => {
  return (
    <div className="px-4 py-3 sm:px-6 sm:py-4 border-b border-gray-100 bg-white/80 backdrop-blur-md flex items-center justify-between sticky top-0 z-10">
      <div className="flex items-center gap-3 sm:gap-4">
        <button 
          onClick={onMenuClick}
          className="md:hidden p-2 -ml-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 flex items-center justify-center">
          <Bot className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600" />
        </div>
        <div>
          <h2 className="text-sm sm:text-base font-semibold text-gray-900 flex items-center gap-2">
            Customer Support Assistant
          </h2>
          <div className="flex items-center gap-2 text-xs text-gray-500">
            {isOnline ? (
              <span className="flex items-center gap-1 text-green-600">
                <Wifi className="w-3 h-3" /> Online
              </span>
            ) : (
              <span className="flex items-center gap-1 text-red-500">
                <WifiOff className="w-3 h-3" /> Offline
              </span>
            )}
            {sessionId && (
              <>
                <span className="w-1 h-1 rounded-full bg-gray-300" />
                <span className="truncate max-w-[100px] sm:max-w-[200px]" title={sessionId}>
                  Session: {sessionId.substring(0, 8)}...
                </span>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatHeader;
