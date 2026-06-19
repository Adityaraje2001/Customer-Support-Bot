import authApi from '../api/authApi';
import type { DocumentResponse } from '../types/knowledge';

export const knowledgeService = {
  uploadDocument: async (file: File, documentType: string, version: string): Promise<DocumentResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);
    formData.append('version', version);

    const response = await authApi.post<DocumentResponse>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getAllDocuments: async (): Promise<DocumentResponse[]> => {
    const response = await authApi.get<DocumentResponse[]>('/documents/');
    return response.data;
  },

  activateDocument: async (documentId: number): Promise<DocumentResponse> => {
    const response = await authApi.patch<DocumentResponse>(`/documents/${documentId}/activate`);
    return response.data;
  },

  archiveDocument: async (documentId: number): Promise<DocumentResponse> => {
    const response = await authApi.patch<DocumentResponse>(`/documents/${documentId}/archive`);
    return response.data;
  },

  softDeleteDocument: async (documentId: number): Promise<void> => {
    await authApi.delete(`/documents/${documentId}`);
  },

  getDocumentHistory: async (documentId: number): Promise<DocumentResponse[]> => {
    const response = await authApi.get<DocumentResponse[]>(`/documents/${documentId}/history`);
    return response.data;
  },

  getDocumentAudit: async (documentId: number): Promise<import('../types/knowledge').DocumentAudit[]> => {
    const response = await authApi.get<import('../types/knowledge').DocumentAudit[]>(`/documents/${documentId}/audit`);
    return response.data;
  },

  rollbackDocument: async (documentId: number, targetVersionId: number): Promise<DocumentResponse> => {
    const response = await authApi.post<DocumentResponse>(`/documents/${documentId}/rollback`, {
      target_version_id: targetVersionId
    });
    return response.data;
  }
};
