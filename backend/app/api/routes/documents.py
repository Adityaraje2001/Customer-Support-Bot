from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.database import SessionLocal
from app.auth.rbac import require_admin
from app.models.user import User
from app.services.document_service import DocumentService
from app.services.audit_service import AuditService
from app.schemas.document import DocumentResponse, DocumentAuditResponse

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

class RollbackRequest(BaseModel):
    target_version_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("general"),
    version: str = Form(""), # Kept for backwards compatibility but ignored by service
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return await service.create_document(file, document_type, version, int(current_user.id))  # type: ignore

@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.list_documents()

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.get_document(document_id)

@router.get("/{document_id}/history", response_model=list[DocumentResponse])
def get_document_history(
    document_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.get_document_history(document_id)

@router.post("/{document_id}/rollback", response_model=DocumentResponse)
def rollback_document(
    document_id: int,
    request: RollbackRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.rollback_document(document_id, request.target_version_id, int(current_user.id))  # type: ignore

@router.get("/{document_id}/audit", response_model=list[DocumentAuditResponse])
def get_document_audit(
    document_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    audit_service = AuditService(db)
    return audit_service.get_document_audit_trail(document_id)

@router.patch("/{document_id}/activate", response_model=DocumentResponse)
def activate_document(
    document_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.activate_document(document_id, performed_by=int(current_user.id))  # type: ignore

@router.patch("/{document_id}/archive", response_model=DocumentResponse)
def archive_document(
    document_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.archive_document(document_id, performed_by=int(current_user.id))  # type: ignore

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    service = DocumentService(db)
    return service.soft_delete_document(document_id, performed_by=int(current_user.id))  # type: ignore
