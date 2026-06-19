import React from 'react';
import ChatContainer from '../components/chat/ChatContainer';

const ChatPage: React.FC = () => {
  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-white overflow-hidden">
      <ChatContainer />
    </div>
  );
};

export default ChatPage;
