"""
SQLAlchemy Document model for Knowledge Base Management System.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_group = Column(String, index=True, nullable=False)
    filename = Column(String, unique=True, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    document_type = Column(String, index=True, nullable=False)
    version = Column(String, nullable=False)
    previous_version_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    status = Column(String, index=True, nullable=False, default="active")
    file_path = Column(String, nullable=False)
    chunk_count = Column(Integer, default=0)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    activated_at = Column(DateTime, nullable=True)
    archived_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False, index=True)

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, group='{self.document_group}', version='{self.version}', status='{self.status}')>"
