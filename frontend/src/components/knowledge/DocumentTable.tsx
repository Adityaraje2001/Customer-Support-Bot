import React from 'react';
import type { DocumentResponse } from '../../types/knowledge';
import DocumentVersionBadge from './DocumentVersionBadge';
import DocumentActions from './DocumentActions';

interface Props {
  documents: DocumentResponse[];
  onActivate: (id: number) => void;
  onArchive: (id: number) => void;
  onDelete: (id: number) => void;
  onViewHistory?: (doc: DocumentResponse) => void;
}

const DocumentTable: React.FC<Props> = ({ documents, onActivate, onArchive, onDelete, onViewHistory }) => {
  return (
    <div className="overflow-x-auto bg-white rounded-xl shadow-sm border border-gray-100">
      <table className="w-full text-sm text-left text-gray-500">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50 border-b border-gray-200">
          <tr>
            <th scope="col" className="px-6 py-4 font-semibold">Filename</th>
            <th scope="col" className="px-6 py-4 font-semibold">Type</th>
            <th scope="col" className="px-6 py-4 font-semibold">Status & Version</th>
            <th scope="col" className="px-6 py-4 font-semibold">Chunks</th>
            <th scope="col" className="px-6 py-4 font-semibold">Uploaded At</th>
            <th scope="col" className="px-6 py-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {documents.length === 0 ? (
            <tr>
              <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                <div className="flex flex-col items-center justify-center">
                  <svg className="w-12 h-12 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                  <p className="text-base font-medium">No documents found</p>
                  <p className="text-sm">Upload a new document to get started.</p>
                </div>
              </td>
            </tr>
          ) : (
            documents.map((doc) => (
              <tr key={doc.id} className="bg-white hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                  {doc.original_filename}
                </td>
                <td className="px-6 py-4">
                  <span className="bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-1 rounded-md border border-gray-200">
                    {doc.document_type.replace('_', ' ').toUpperCase()}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <DocumentVersionBadge status={doc.status} version={doc.version} />
                </td>
                <td className="px-6 py-4 text-gray-600 font-medium">
                  {doc.chunk_count}
                </td>
                <td className="px-6 py-4 text-gray-500">
                  {new Date(doc.uploaded_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4">
                  <DocumentActions 
                    document={doc}
                    onActivate={onActivate}
                    onArchive={onArchive}
                    onDelete={onDelete}
                    onViewHistory={onViewHistory}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default DocumentTable;
