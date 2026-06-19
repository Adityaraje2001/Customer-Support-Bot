from sqlalchemy.orm import Session
from app.models.document_audit import DocumentAudit
from typing import Optional, Any

class AuditService:
    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        document_id: int,
        action: str,
        performed_by: int,
        metadata_info: Optional[dict[str, Any]] = None
    ) -> DocumentAudit:
        """
        Create an audit log entry for a document action.
        Actions: UPLOAD, ACTIVATE, ARCHIVE, ROLLBACK, DELETE
        """
        audit_entry = DocumentAudit(
            document_id=document_id,
            action=action,
            performed_by=performed_by,
            metadata_info=metadata_info
        )
        self.db.add(audit_entry)
        self.db.commit()
        self.db.refresh(audit_entry)
        return audit_entry

    def get_document_audit_trail(self, document_id: int):
        return self.db.query(DocumentAudit)\
            .filter(DocumentAudit.document_id == document_id)\
            .order_by(DocumentAudit.timestamp.desc())\
            .all()
