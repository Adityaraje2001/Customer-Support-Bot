from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class DocumentResponse(BaseModel):
    id: int
    document_group: str
    filename: str
    original_filename: str
    document_type: str
    version: str
    previous_version_id: Optional[int] = None
    status: str
    file_path: str
    chunk_count: int
    uploaded_by: int
    uploaded_at: datetime
    updated_at: datetime
    activated_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    total: int

class DocumentAuditResponse(BaseModel):
    id: int
    document_id: int
    action: str
    performed_by: int
    timestamp: datetime
    metadata_info: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class DocumentHistoryResponse(BaseModel):
    items: list[DocumentResponse]
    total: int
