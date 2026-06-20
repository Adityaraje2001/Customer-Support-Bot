import React, { useState } from 'react';
import { User, Bot, Copy, Check, ThumbsUp, ThumbsDown } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import type { Message } from '../../types/chat';
import AgentBadge from './AgentBadge';
import FeedbackModal from './FeedbackModal';

interface ChatMessageProps {
  message: Message;
  onFeedback?: (
    messageId: string,
    feedbackType: 'helpful' | 'not_helpful',
    comment?: string,
  ) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onFeedback }) => {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const feedbackGiven = message.feedbackGiven;

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleThumbsUp = () => {
    if (feedbackGiven) return;
    onFeedback?.(message.id, 'helpful');
  };

  const handleThumbsDown = () => {
    if (feedbackGiven) return;
    setShowModal(true);
  };

  const handleModalSubmit = (comment: string) => {
    setShowModal(false);
    onFeedback?.(message.id, 'not_helpful', comment || undefined);
  };

  const formattedTime = new Date(message.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <>
      <div className={`flex gap-3 sm:gap-4 w-full ${isUser ? 'flex-row-reverse' : ''} group animate-in fade-in slide-in-from-bottom-2`}>
        <div
          className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-sm ${
            isUser ? 'bg-blue-600' : 'bg-gray-800'
          }`}
        >
          {isUser ? <User className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4 text-white" />}
        </div>

        <div className={`flex flex-col max-w-[85%] sm:max-w-[75%] ${isUser ? 'items-end' : 'items-start'}`}>
          {!isUser && message.agentUsed && <AgentBadge agentName={message.agentUsed} />}

          <div className="relative group/message">
            <div
              className={`px-4 sm:px-5 py-3 sm:py-3.5 rounded-2xl text-[14px] sm:text-[15px] leading-relaxed ${
                isUser
                  ? 'bg-blue-600 text-white rounded-tr-sm'
                  : 'bg-white text-gray-800 shadow-sm border border-gray-100 rounded-tl-sm'
              }`}
            >
              {isUser ? (
                <p className="whitespace-pre-wrap">{message.content}</p>
              ) : (
                <div className="prose prose-sm max-w-none prose-p:leading-relaxed prose-pre:p-0 prose-pre:bg-transparent prose-pre:m-0">
                  <ReactMarkdown
                    components={{
                      code({ node, inline, className, children, ...props }: any) {
                        const match = /language-(\w+)/.exec(className || '');
                        return !inline && match ? (
                          <div className="rounded-lg overflow-hidden my-3 border border-gray-700 bg-[#1E1E1E]">
                            <div className="flex items-center justify-between px-4 py-1.5 bg-[#2D2D2D] border-b border-gray-700">
                              <span className="text-xs text-gray-300 font-mono lowercase">{match[1]}</span>
                            </div>
                            <SyntaxHighlighter
                              {...props}
                              style={vscDarkPlus as any}
                              language={match[1]}
                              PreTag="div"
                              customStyle={{ margin: 0, borderRadius: 0, padding: '1rem' }}
                            >
                              {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                          </div>
                        ) : (
                          <code {...props} className={`${className} px-1.5 py-0.5 rounded-md bg-gray-100 text-pink-600 font-mono text-[13px]`}>
                            {children}
                          </code>
                        );
                      },
                      p: ({ children }) => <p className="mb-3 last:mb-0">{children}</p>,
                      ul: ({ children }) => <ul className="list-disc pl-5 mb-3 last:mb-0 space-y-1">{children}</ul>,
                      ol: ({ children }) => <ol className="list-decimal pl-5 mb-3 last:mb-0 space-y-1">{children}</ol>,
                      h1: ({ children }) => <h1 className="text-xl font-bold mb-3 mt-4 first:mt-0">{children}</h1>,
                      h2: ({ children }) => <h2 className="text-lg font-bold mb-2 mt-4 first:mt-0">{children}</h2>,
                      h3: ({ children }) => <h3 className="text-md font-bold mb-2 mt-3 first:mt-0">{children}</h3>,
                      table: ({ children }) => (
                        <div className="overflow-x-auto my-3">
                          <table className="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg overflow-hidden">
                            {children}
                          </table>
                        </div>
                      ),
                      th: ({ children }) => <th className="bg-gray-50 px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{children}</th>,
                      td: ({ children }) => <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-500 border-t border-gray-100">{children}</td>,
                    }}
                  >
                    {message.content || ' '}
                  </ReactMarkdown>
                </div>
              )}
            </div>

            {/* Copy Button */}
            {!isUser && (
              <button
                onClick={handleCopy}
                className="absolute -right-10 top-2 p-1.5 text-gray-400 hover:text-gray-600 bg-white shadow-sm border border-gray-100 rounded-md opacity-0 group-hover/message:opacity-100 transition-opacity"
                title="Copy message"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-green-500" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
            )}
          </div>

          {/* Feedback Buttons */}
          {!isUser && (
            <div className="flex items-center gap-1 mt-1.5 px-1">
              <span className="text-[11px] text-gray-400 font-medium mr-1">
                {formattedTime}
              </span>

              {feedbackGiven ? (
                <span className={`inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full ${
                  feedbackGiven === 'helpful'
                    ? 'bg-green-50 text-green-600'
                    : 'bg-red-50 text-red-500'
                }`}>
                  {feedbackGiven === 'helpful' ? (
                    <><ThumbsUp className="w-3 h-3" /> Helpful</>
                  ) : (
                    <><ThumbsDown className="w-3 h-3" /> Not Helpful</>
                  )}
                </span>
              ) : (
                <>
                  <button
                    id={`feedback-helpful-${message.id}`}
                    onClick={handleThumbsUp}
                    className="p-1 rounded-md text-gray-300 hover:text-green-500 hover:bg-green-50 transition-all"
                    title="Helpful"
                  >
                    <ThumbsUp className="w-3.5 h-3.5" />
                  </button>
                  <button
                    id={`feedback-not-helpful-${message.id}`}
                    onClick={handleThumbsDown}
                    className="p-1 rounded-md text-gray-300 hover:text-red-500 hover:bg-red-50 transition-all"
                    title="Not Helpful"
                  >
                    <ThumbsDown className="w-3.5 h-3.5" />
                  </button>
                </>
              )}
            </div>
          )}

          {/* Timestamp for user messages */}
          {isUser && (
            <span className="text-[11px] text-gray-400 mt-1.5 px-1 font-medium">
              {formattedTime}
            </span>
          )}
        </div>
      </div>

      {/* Negative Feedback Modal */}
      <FeedbackModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onSubmit={handleModalSubmit}
      />
    </>
  );
};

export default ChatMessage;
