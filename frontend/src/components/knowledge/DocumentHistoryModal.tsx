import React, { useEffect, useState } from 'react';
import type { DocumentResponse, DocumentAudit } from '../../types/knowledge';
import { knowledgeService } from '../../services/knowledgeService';
import DocumentVersionBadge from './DocumentVersionBadge';
import toast from 'react-hot-toast';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  document: DocumentResponse | null;
  onRollbackSuccess: () => void;
}

const DocumentHistoryModal: React.FC<Props> = ({ isOpen, onClose, document, onRollbackSuccess }) => {
  const [history, setHistory] = useState<DocumentResponse[]>([]);
  const [audits, setAudits] = useState<DocumentAudit[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'history' | 'audit'>('history');

  useEffect(() => {
    if (isOpen && document) {
      fetchData();
    }
  }, [isOpen, document]);

  const fetchData = async () => {
    if (!document) return;
    try {
      setIsLoading(true);
      const [historyData, auditData] = await Promise.all([
        knowledgeService.getDocumentHistory(document.id),
        knowledgeService.getDocumentAudit(document.id)
      ]);
      setHistory(historyData);
      setAudits(auditData);
    } catch (error) {
      toast.error('Failed to load history');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRollback = async (targetVersionId: number) => {
    if (!document) return;
    if (window.confirm('Are you sure you want to rollback to this version?')) {
      try {
        await knowledgeService.rollbackDocument(document.id, targetVersionId);
        toast.success('Document rolled back successfully');
        onRollbackSuccess();
        onClose();
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Failed to rollback');
      }
    }
  };

  if (!isOpen || !document) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity" aria-hidden="true" onClick={onClose}>
          <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
        </div>

        <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="sm:flex sm:items-start">
              <div className="mt-3 text-center sm:mt-0 sm:text-left w-full">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                  History & Lifecycle: {document.original_filename}
                </h3>

                <div className="border-b border-gray-200 mb-4">
                  <nav className="-mb-px flex space-x-8">
                    <button
                      onClick={() => setActiveTab('history')}
                      className={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${
                        activeTab === 'history'
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      Version History
                    </button>
                    <button
                      onClick={() => setActiveTab('audit')}
                      className={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${
                        activeTab === 'audit'
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      Audit Trail
                    </button>
                  </nav>
                </div>

                {isLoading ? (
                  <div className="flex justify-center items-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  </div>
                ) : (
                  <div className="max-h-96 overflow-y-auto">
                    {activeTab === 'history' && (
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Version</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uploaded / Activated</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {history.map((doc) => (
                            <tr key={doc.id}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                {doc.version}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                <DocumentVersionBadge status={doc.status} version={doc.version} />
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                <div>Up: {new Date(doc.uploaded_at).toLocaleDateString()}</div>
                                {doc.activated_at && <div>Act: {new Date(doc.activated_at).toLocaleDateString()}</div>}
                                {doc.archived_at && <div>Arch: {new Date(doc.archived_at).toLocaleDateString()}</div>}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                {doc.status !== 'active' && doc.status !== 'deleted' && (
                                  <button
                                    onClick={() => handleRollback(doc.id)}
                                    className="text-blue-600 hover:text-blue-900 font-semibold"
                                  >
                                    Rollback to {doc.version}
                                  </button>
                                )}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}

                    {activeTab === 'audit' && (
                      <div className="flow-root">
                        <ul className="-mb-8">
                          {audits.map((audit, eventIdx) => (
                            <li key={audit.id}>
                              <div className="relative pb-8">
                                {eventIdx !== audits.length - 1 ? (
                                  <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true"></span>
                                ) : null}
                                <div className="relative flex space-x-3">
                                  <div>
                                    <span className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center ring-8 ring-white">
                                      <svg className="h-4 w-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                      </svg>
                                    </span>
                                  </div>
                                  <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                                    <div>
                                      <p className="text-sm text-gray-500">
                                        <span className="font-medium text-gray-900">{audit.action}</span>
                                        {' '}by User ID {audit.performed_by}
                                        {audit.metadata_info && audit.metadata_info.rolled_back_from_version && (
                                          <span> (From {audit.metadata_info.rolled_back_from_version})</span>
                                        )}
                                      </p>
                                    </div>
                                    <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                      <time dateTime={audit.timestamp}>{new Date(audit.timestamp).toLocaleDateString()}</time>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              onClick={onClose}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentHistoryModal;
