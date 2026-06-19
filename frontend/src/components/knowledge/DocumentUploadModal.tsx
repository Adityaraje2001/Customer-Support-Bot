import React, { useState } from 'react';
import { knowledgeService } from '../../services/knowledgeService';
import toast from 'react-hot-toast';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: () => void;
}

const DocumentUploadModal: React.FC<Props> = ({ isOpen, onClose, onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState('general');
  const [version, setVersion] = useState('v1');
  const [isUploading, setIsUploading] = useState(false);

  if (!isOpen) return null;

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      toast.error('Please select a file');
      return;
    }

    try {
      setIsUploading(true);
      await knowledgeService.uploadDocument(file, documentType, version);
      toast.success('Document uploaded successfully');
      onUploadSuccess();
      onClose();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to upload document');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900 bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md p-6 animate-in fade-in zoom-in duration-200">
        <h2 className="text-xl font-semibold mb-4 text-gray-900">Upload Document</h2>
        <form onSubmit={handleUpload}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">File (PDF)</label>
            <input
              type="file"
              accept=".pdf"
              className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-colors"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Document Type</label>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition-colors"
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
              required
            >
              <option value="refund_policy">Refund Policy</option>
              <option value="billing_policy">Billing Policy</option>
              <option value="shipping_policy">Shipping Policy</option>
              <option value="faq">FAQ</option>
              <option value="general">General</option>
            </select>
          </div>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">Version (e.g., v1, v2)</label>
            <input
              type="text"
              placeholder="v1"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition-colors"
              value={version}
              onChange={(e) => setVersion(e.target.value)}
              required
            />
          </div>
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-4 focus:ring-gray-100 transition-colors"
              disabled={isUploading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 disabled:opacity-50 transition-colors flex items-center"
              disabled={isUploading}
            >
              {isUploading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Uploading...
                </>
              ) : 'Upload'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DocumentUploadModal;
