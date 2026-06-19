import React from 'react';

interface SuggestedPromptsProps {
  onSelect: (prompt: string) => void;
}

const SuggestedPrompts: React.FC<SuggestedPromptsProps> = ({ onSelect }) => {
  const prompts = [
    "How long do refunds take?",
    "Create a refund ticket",
    "What is the status of ticket #1?",
    "I need help with billing",
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl mx-auto mt-8">
      {prompts.map((prompt, index) => (
        <button
          key={index}
          onClick={() => onSelect(prompt)}
          className="text-left px-4 py-3 bg-white border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50/50 hover:shadow-sm transition-all duration-200 text-sm text-gray-700 font-medium group"
        >
          <span className="group-hover:text-blue-600 transition-colors">{prompt}</span>
        </button>
      ))}
    </div>
  );
};

export default SuggestedPrompts;
