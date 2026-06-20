import logging
from datetime import datetime, timezone
from app.celery_app import celery_app
from app.database.database import SessionLocal
from app.models.document import Document
from app.models.user import User  # Needed for SQLAlchemy to resolve the users table foreign key
from app.pipelines.ingestion_pipeline import IngestionPipeline
from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.embeddings import EmbeddingService
from app.ingestion.text_splitter import TextSplitter
from app.ingestion.pdf_loader import PDFLoader

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def process_document_task(self, document_id: int):
    """
    Background task to process and ingest a document.
    """
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            logger.error(f"Document {document_id} not found.")
            return

        # Update status to processing
        doc.status = "processing"
        doc.processing_started_at = datetime.now(timezone.utc)
        db.commit()
        
        # Start MLflow run
        import contextlib
        from app.monitoring.mlflow_tracker import mlflow_tracker
        
        run = mlflow_tracker.start_run(run_name=f"ingest_document_{document_id}")
        with run or contextlib.nullcontext():
            mlflow_tracker.log_param("document_id", document_id)
            mlflow_tracker.log_param("filename", str(doc.filename))

            try:
                pipeline = IngestionPipeline(
                    pdf_loader=PDFLoader(),
                    text_splitter=TextSplitter(),
                    embedding_service=EmbeddingService(),
                    vectorstore=ChromaStore()
                )

                summary = pipeline.ingest_pdf(
                    pdf_path=str(doc.file_path), # type: ignore
                    document_id=str(doc.filename), # type: ignore
                    user_id=int(doc.uploaded_by), # type: ignore
                    metadata_overrides={
                        "status": "active", 
                        "is_active": True, 
                        "db_document_id": doc.id, 
                        "document_group": doc.document_group
                    }
                )

                # Update document on success
                doc.chunk_count = summary["chunks_created"]
                doc.status = "active"
                doc.is_active = True
                doc.processing_completed_at = datetime.now(timezone.utc)
                db.commit()
                
                mlflow_tracker.log_metric("chunks_created", float(summary["chunks_created"]))
                mlflow_tracker.log_param("status", "success")
                logger.info(f"Successfully processed document {document_id}")

            except Exception as e:
                logger.error(f"Error processing document {document_id}: {str(e)}")
                mlflow_tracker.log_param("status", "failed")
                mlflow_tracker.log_param("error", str(e))
                
                # Retry
                raise self.retry(exc=e, countdown=10)

    except Exception as e:
        # If it exhausts retries or fails outside the pipeline
        logger.error(f"Task failed for document {document_id}: {str(e)}")
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = "failed"
            doc.error_message = str(e)
            db.commit()
        raise e
    finally:
        db.close()
