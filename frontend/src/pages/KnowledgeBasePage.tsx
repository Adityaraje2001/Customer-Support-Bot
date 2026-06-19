import React, { useEffect, useState } from 'react';
import type { DocumentResponse } from '../types/knowledge';
import { knowledgeService } from '../services/knowledgeService';
import KnowledgeBaseStats from '../components/knowledge/KnowledgeBaseStats';
import DocumentFilters from '../components/knowledge/DocumentFilters';
import DocumentTable from '../components/knowledge/DocumentTable';
import DocumentUploadModal from '../components/knowledge/DocumentUploadModal';
import DocumentHistoryModal from '../components/knowledge/DocumentHistoryModal';
import toast from 'react-hot-toast';

const KnowledgeBasePage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [historyModalOpen, setHistoryModalOpen] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState<DocumentResponse | null>(null);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [documentType, setDocumentType] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  const fetchDocuments = async () => {
    try {
      setIsLoading(true);
      const data = await knowledgeService.getAllDocuments();
      setDocuments(data);
    } catch (error) {
      toast.error('Failed to fetch documents');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleActivate = async (id: number) => {
    try {
      await knowledgeService.activateDocument(id);
      toast.success('Document activated');
      fetchDocuments();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to activate document');
    }
  };

  const handleArchive = async (id: number) => {
    try {
      await knowledgeService.archiveDocument(id);
      toast.success('Document archived');
      fetchDocuments();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to archive document');
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await knowledgeService.softDeleteDocument(id);
      toast.success('Document deleted');
      fetchDocuments();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to delete document');
    }
  };

  const handleViewHistory = (doc: DocumentResponse) => {
    setSelectedDocument(doc);
    setHistoryModalOpen(true);
  };

  const filteredDocuments = documents.filter((doc) => {
    const matchesSearch = doc.filename.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          doc.original_filename.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = documentType === 'all' || doc.document_type === documentType;
    const matchesStatus = statusFilter === 'all' || doc.status === statusFilter;
    return matchesSearch && matchesType && matchesStatus;
  });

  return (
    <div className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 animate-in fade-in duration-300">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Knowledge Base</h1>
          <p className="mt-1 text-sm text-gray-500">Manage RAG documents and company policies</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
        >
          <svg className="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Upload Document
        </button>
      </div>

      <KnowledgeBaseStats documents={documents} />

      <DocumentFilters 
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        documentType={documentType}
        setDocumentType={setDocumentType}
        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}
      />

      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <DocumentTable 
          documents={filteredDocuments}
          onActivate={handleActivate}
          onArchive={handleArchive}
          onDelete={handleDelete}
          onViewHistory={handleViewHistory}
        />
      )}

      <DocumentUploadModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onUploadSuccess={fetchDocuments}
      />

      <DocumentHistoryModal
        isOpen={historyModalOpen}
        onClose={() => setHistoryModalOpen(false)}
        document={selectedDocument}
        onRollbackSuccess={fetchDocuments}
      />
    </div>
  );
};

export default KnowledgeBasePage;
