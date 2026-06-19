import React from 'react';
import type { DocumentResponse } from '../../types/knowledge';

interface Props {
  document: DocumentResponse;
  onActivate: (id: number) => void;
  onArchive: (id: number) => void;
  onDelete: (id: number) => void;
  onViewHistory?: (doc: DocumentResponse) => void;
}

const DocumentActions: React.FC<Props> = ({ document, onActivate, onArchive, onDelete, onViewHistory }) => {
  return (
    <div className="flex items-center justify-end space-x-2">
      {onViewHistory && (
        <button
          onClick={() => onViewHistory(document)}
          className="px-3 py-1.5 text-sm font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-md transition-colors"
          title="View History"
        >
          History
        </button>
      )}
      {document.status !== 'active' && document.status !== 'deleted' && (
        <button
          onClick={() => onActivate(document.id)}
          className="px-3 py-1.5 text-sm font-medium text-green-700 bg-green-50 hover:bg-green-100 rounded-md transition-colors"
          title="Activate"
        >
          Activate
        </button>
      )}
      {document.status !== 'archived' && document.status !== 'deleted' && (
        <button
          onClick={() => onArchive(document.id)}
          className="px-3 py-1.5 text-sm font-medium text-yellow-700 bg-yellow-50 hover:bg-yellow-100 rounded-md transition-colors"
          title="Archive"
        >
          Archive
        </button>
      )}
      {document.status !== 'deleted' && (
        <button
          onClick={() => {
            if (window.confirm(`Are you sure you want to delete ${document.filename}?`)) {
              onDelete(document.id);
            }
          }}
          className="px-3 py-1.5 text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-md transition-colors"
          title="Delete"
        >
          Delete
        </button>
      )}
    </div>
  );
};

export default DocumentActions;
