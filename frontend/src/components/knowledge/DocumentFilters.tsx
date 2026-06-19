import React from 'react';

interface Props {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  documentType: string;
  setDocumentType: (type: string) => void;
  statusFilter: string;
  setStatusFilter: (status: string) => void;
}

const DocumentFilters: React.FC<Props> = ({ searchTerm, setSearchTerm, documentType, setDocumentType, statusFilter, setStatusFilter }) => {
  return (
    <div className="flex flex-col md:flex-row gap-4 mb-6 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
      <div className="flex-1">
        <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
        <input
          type="text"
          placeholder="Search filename or type..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition-colors"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <div className="w-full md:w-48">
        <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
        <select
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-white"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="all">All Statuses</option>
          <option value="active">Active</option>
          <option value="archived">Archived</option>
          <option value="deleted">Deleted</option>
        </select>
      </div>
      <div className="w-full md:w-48">
        <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
        <select
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 bg-white"
          value={documentType}
          onChange={(e) => setDocumentType(e.target.value)}
        >
          <option value="all">All Types</option>
          <option value="refund_policy">Refund Policy</option>
          <option value="billing_policy">Billing Policy</option>
          <option value="shipping_policy">Shipping Policy</option>
          <option value="faq">FAQ</option>
          <option value="general">General</option>
        </select>
      </div>
    </div>
  );
};

export default DocumentFilters;
