export interface DocumentResponse {
  id: number;
  document_group: string;
  filename: string;
  original_filename: string;
  document_type: string;
  version: string;
  previous_version_id: number | null;
  status: 'pending' | 'processing' | 'active' | 'archived' | 'deleted' | 'failed';
  file_path: string;
  chunk_count: number;
  uploaded_by: number;
  uploaded_at: string;
  updated_at: string;
  activated_at: string | null;
  archived_at: string | null;
  deleted_at: string | null;
  is_active: boolean;
}

export interface DocumentAudit {
  id: number;
  document_id: number;
  action: 'UPLOAD' | 'ACTIVATE' | 'ARCHIVE' | 'ROLLBACK' | 'DELETE';
  performed_by: number;
  timestamp: string;
  metadata_info: Record<string, any> | null;
}
