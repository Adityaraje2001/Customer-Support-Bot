from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class DocumentAudit(Base):
    __tablename__ = "document_audits"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True, nullable=False)
    action = Column(String, index=True, nullable=False) # UPLOAD, ACTIVATE, ARCHIVE, ROLLBACK, DELETE
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    metadata_info = Column(JSONB, nullable=True) # Renamed from metadata to avoid conflict with SQLAlchemy Base.metadata

    def __repr__(self) -> str:
        return f"<DocumentAudit(id={self.id}, doc_id={self.document_id}, action='{self.action}')>"
