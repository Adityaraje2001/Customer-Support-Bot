import React, { useEffect, useState, useMemo } from 'react';
import { conversationService } from '../services/conversationService';
import type { Conversation, ConversationFilter } from '../types/conversation';
import ConversationList from '../components/conversations/ConversationList';
import ConversationViewer from '../components/conversations/ConversationViewer';
import ConversationFilters from '../components/conversations/ConversationFilters';
import ConversationEmptyState from '../components/conversations/ConversationEmptyState';
import toast from 'react-hot-toast';

const ConversationHistoryPage: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [loadingList, setLoadingList] = useState(true);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState<ConversationFilter>('All');

  // Mobile view state
  const [showViewerOnMobile, setShowViewerOnMobile] = useState(false);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      setLoadingList(true);
      const data = await conversationService.getConversations();
      setConversations(data);
    } catch (error) {
      toast.error('Failed to load conversations');
    } finally {
      setLoadingList(false);
    }
  };

  const handleSelectConversation = async (id: string) => {
    try {
      setLoadingMessages(true);
      setShowViewerOnMobile(true);
      
      const conv = conversations.find(c => c.id === id);
      if (!conv) return;

      const messages = await conversationService.getConversationMessages(id);
      setSelectedConversation({ ...conv, messages });
    } catch (error) {
      toast.error('Failed to load messages');
    } finally {
      setLoadingMessages(false);
    }
  };

  const handleDeleteConversation = async (id: string) => {
    try {
      await conversationService.deleteConversation(id);
      setConversations(prev => prev.filter(c => c.id !== id));
      if (selectedConversation?.id === id) {
        setSelectedConversation(null);
        setShowViewerOnMobile(false);
      }
      toast.success('Conversation deleted');
    } catch (error) {
      toast.error('Failed to delete conversation');
    }
  };

  const filteredConversations = useMemo(() => {
    let result = conversations;

    if (searchTerm) {
      result = result.filter(c => 
        c.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    const now = new Date();
    if (activeFilter === 'Today') {
      result = result.filter(c => new Date(c.createdAt).toDateString() === now.toDateString());
    } else if (activeFilter === 'Last 7 Days') {
      const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
      result = result.filter(c => new Date(c.createdAt) >= weekAgo);
    } else if (activeFilter === 'Last 30 Days') {
      const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
      result = result.filter(c => new Date(c.createdAt) >= monthAgo);
    }

    // Sort by most recent
    return result.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
  }, [conversations, searchTerm, activeFilter]);

  return (
    <div className="flex flex-col h-[calc(100vh-2rem)] bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="flex h-full relative">
        {/* Sidebar List */}
        <div 
          className={`flex-shrink-0 w-full md:w-80 lg:w-96 border-r border-gray-200 bg-gray-50 flex flex-col ${
            showViewerOnMobile ? 'hidden md:flex' : 'flex'
          }`}
        >
          <div className="p-4 border-b border-gray-200 bg-white">
            <h2 className="text-xl font-bold text-gray-900">Conversations</h2>
            <p className="text-sm text-gray-500">View your chat history</p>
          </div>
          
          <ConversationFilters
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            activeFilter={activeFilter}
            onFilterChange={setActiveFilter}
          />

          <div className="flex-1 overflow-y-auto">
            {filteredConversations.length > 0 || loadingList ? (
              <ConversationList
                conversations={filteredConversations}
                selectedId={selectedConversation?.id || null}
                onSelect={handleSelectConversation}
                loading={loadingList}
              />
            ) : (
              <div className="p-8 text-center text-gray-500">
                <p>No conversations found matching your filters.</p>
              </div>
            )}
          </div>
        </div>

        {/* Main Viewer area */}
        <div className={`flex-1 flex flex-col min-w-0 ${showViewerOnMobile ? 'flex' : 'hidden md:flex'}`}>
          {/* Mobile Back Button */}
          {showViewerOnMobile && (
            <div className="md:hidden p-4 border-b border-gray-200 bg-white">
              <button 
                onClick={() => setShowViewerOnMobile(false)}
                className="text-blue-600 font-medium text-sm flex items-center"
              >
                ← Back to List
              </button>
            </div>
          )}

          {selectedConversation ? (
            <ConversationViewer
              conversation={selectedConversation}
              loading={loadingMessages}
              onDelete={handleDeleteConversation}
            />
          ) : (
            <ConversationEmptyState />
          )}
        </div>
      </div>
    </div>
  );
};

export default ConversationHistoryPage;
