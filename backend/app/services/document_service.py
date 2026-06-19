import logging
import re
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.models.document import Document
from app.services.file_service import FileService
from app.services.audit_service import AuditService
from app.pipelines.ingestion_pipeline import IngestionPipeline
from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.embeddings import EmbeddingService
from app.ingestion.text_splitter import TextSplitter
from app.ingestion.pdf_loader import PDFLoader

logger = logging.getLogger(__name__)

def extract_document_group(filename: str) -> str:
    """
    Extracts a document group name from a filename.
    Examples:
    - Refund_Policy.pdf -> refund_policy
    - Refund_Policy_New.pdf -> refund_policy
    - refund_policy_v2.pdf -> refund_policy
    """
    base_name = filename.rsplit('.', 1)[0]
    base_name = base_name.lower()
    # Remove _new, _vX, etc.
    base_name = re.sub(r'_(new|v\d+|\d+)$', '', base_name)
    return base_name

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.file_service = FileService()
        self.chroma_store = ChromaStore()
        self.audit_service = AuditService(db)
        
        # We can initialize ingestion pipeline here or in a separate factory
        self.ingestion_pipeline = IngestionPipeline(
            pdf_loader=PDFLoader(),
            text_splitter=TextSplitter(),
            embedding_service=EmbeddingService(),
            vectorstore=self.chroma_store,
        )

    def get_latest_version(self, document_group: str):
        return self.db.query(Document).filter(
            Document.document_group == document_group
        ).order_by(Document.id.desc()).first()

    def generate_next_version(self, document_group: str) -> str:
        latest = self.get_latest_version(document_group)
        if not latest:
            return "v1"
        try:
            current_num = int(latest.version.lstrip("v"))
            return f"v{current_num + 1}"
        except ValueError:
            return f"{latest.version}_new"

    async def create_document(self, file: UploadFile, document_type: str, version: str, user_id: int):
        # The incoming version string might be ignored in favor of automatic versioning
        original_filename = file.filename or "unknown.pdf"
        document_group = extract_document_group(original_filename)
        
        new_version = self.generate_next_version(document_group)
        latest_doc = self.get_latest_version(document_group)
        previous_version_id = latest_doc.id if latest_doc else None

        # Archive any currently active document of the same group
        active_doc = self.get_active_document_by_group(document_group)
        if active_doc:
            self.archive_document(active_doc.id, performed_by=user_id)

        # Upload the file to storage
        upload_result = await self.file_service.upload_file(file)
        if upload_result["status"] != "completed":
            raise HTTPException(status_code=400, detail="File upload failed")

        filename = upload_result["filename"]
        file_path = upload_result["file_path"]

        # Create DB Record (initial state)
        new_document = Document(
            document_group=document_group,
            filename=filename,
            original_filename=original_filename,
            document_type=document_type,
            version=new_version,
            previous_version_id=previous_version_id,
            status="active",
            file_path=file_path,
            uploaded_by=user_id,
            is_active=True,
            activated_at=datetime.now(timezone.utc),
            chunk_count=0
        )
        self.db.add(new_document)
        self.db.commit()
        self.db.refresh(new_document)

        # Audit Logs
        self.audit_service.log_action(new_document.id, "UPLOAD", user_id)
        self.audit_service.log_action(new_document.id, "ACTIVATE", user_id)

        # Ingest Document
        try:
            summary = self.ingestion_pipeline.ingest_pdf(
                pdf_path=file_path,
                document_id=filename,
                user_id=user_id,
                metadata_overrides={"status": "active", "is_active": True, "db_document_id": new_document.id, "document_group": document_group}
            )
            
            # Update DB with chunk count
            new_document.chunk_count = summary["chunks_created"]
            self.db.commit()
            self.db.refresh(new_document)
            
        except Exception as e:
            # If ingestion fails, we might want to soft delete or mark as failed
            new_document.status = "deleted"
            new_document.is_active = False
            new_document.deleted_at = datetime.now(timezone.utc)
            self.db.commit()
            raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

        return new_document

    def list_documents(self):
        return self.db.query(Document).order_by(Document.uploaded_at.desc()).all()

    def get_document(self, document_id: int):
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc

    def get_document_history(self, document_id: int):
        doc = self.get_document(document_id)
        return self.db.query(Document).filter(
            Document.document_group == doc.document_group
        ).order_by(Document.id.desc()).all()

    def activate_document(self, document_id: int, performed_by: int):
        target_doc = self.get_document(document_id)
        if target_doc.status == "deleted":
            raise HTTPException(status_code=400, detail="Cannot activate a deleted document")

        if target_doc.status == "active":
            return target_doc

        # Archive current active
        active_doc = self.get_active_document_by_group(target_doc.document_group)
        if active_doc and active_doc.id != target_doc.id:
            self.archive_document(active_doc.id, performed_by=performed_by)

        # Activate target
        target_doc.status = "active"
        target_doc.is_active = True
        target_doc.activated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(target_doc)

        self.audit_service.log_action(target_doc.id, "ACTIVATE", performed_by)

        # Update Chroma metadata
        self.chroma_store.update_document_metadata(
            document_id=target_doc.filename,
            update_dict={"status": "active", "is_active": True}
        )

        return target_doc

    def archive_document(self, document_id: int, performed_by: int):
        doc = self.get_document(document_id)
        if doc.status == "deleted":
            raise HTTPException(status_code=400, detail="Cannot archive a deleted document")
        if doc.status == "archived":
            return doc

        doc.status = "archived"
        doc.is_active = False
        doc.archived_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(doc)

        self.audit_service.log_action(doc.id, "ARCHIVE", performed_by)

        self.chroma_store.update_document_metadata(
            document_id=doc.filename,
            update_dict={"status": "archived", "is_active": False}
        )
        return doc

    def soft_delete_document(self, document_id: int, performed_by: int):
        doc = self.get_document(document_id)
        doc.status = "deleted"
        doc.is_active = False
        doc.deleted_at = datetime.now(timezone.utc)
        self.db.commit()

        self.audit_service.log_action(doc.id, "DELETE", performed_by)

        self.chroma_store.update_document_metadata(
            document_id=doc.filename,
            update_dict={"status": "deleted", "is_active": False}
        )
        return {"message": "Document soft deleted"}

    def rollback_document(self, document_id: int, target_version_id: int, performed_by: int):
        target_doc = self.get_document(target_version_id)
        base_doc = self.get_document(document_id)

        if target_doc.document_group != base_doc.document_group:
            raise HTTPException(status_code=400, detail="Cannot rollback to a document from a different group")

        active_doc = self.get_active_document_by_group(target_doc.document_group)
        if active_doc:
            self.archive_document(active_doc.id, performed_by=performed_by)

        # Activate target
        target_doc.status = "active"
        target_doc.is_active = True
        target_doc.activated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(target_doc)

        self.audit_service.log_action(
            target_doc.id, 
            "ROLLBACK", 
            performed_by, 
            metadata_info={"rolled_back_from_version": active_doc.version if active_doc else None}
        )

        self.chroma_store.update_document_metadata(
            document_id=target_doc.filename,
            update_dict={"status": "active", "is_active": True}
        )

        return target_doc

    def get_active_document_by_group(self, document_group: str):
        return self.db.query(Document).filter(
            Document.document_group == document_group,
            Document.status == "active",
            Document.is_active == True
        ).first()

    def get_active_document_by_type(self, document_type: str):
        return self.db.query(Document).filter(
            Document.document_type == document_type,
            Document.status == "active",
            Document.is_active == True
        ).first()
