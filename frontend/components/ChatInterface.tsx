import React, { useState } from 'react';

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    // TODO: Implement backend API call here
    // Example: fetch('/api/chat', { method: 'POST', body: JSON.stringify({ message: input }) })
    if (input.trim() === '') return;
    setMessages([...messages, { role: 'user', content: input }]);
    setInput('');
  };

  return (
    <div className="w-full max-w-2xl mx-auto border rounded-lg overflow-hidden flex flex-col h-[600px] bg-white">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 self-end ml-auto' : 'bg-gray-100'} w-fit max-w-[80%]`}>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="p-4 border-t flex gap-2 bg-gray-50">
        <input 
          type="text" 
          className="flex-1 border p-2 rounded-lg" 
          placeholder="Ask a support question..." 
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition" onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}
