from fastapi import APIRouter, File, HTTPException, Depends
from fastapi import UploadFile as FastAPIUploadFile

from app.auth.dependencies import get_current_user
from app.auth.rbac import require_customer
from app.models.user import User

from app.services.file_service import FileService
from app.schemas.upload import UploadResponse

from app.pipelines.ingestion_pipeline import IngestionPipeline
from app.rag.vectorstores.chroma_store import ChromaStore
from app.rag.embeddings import EmbeddingService
from app.ingestion.text_splitter import TextSplitter
from app.ingestion.pdf_loader import PDFLoader


router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)


@router.post("/", response_model=UploadResponse)
async def upload_document(
    file: FastAPIUploadFile = File(...),
    current_user: User = Depends(require_customer)
):
    """
    Upload a PDF and automatically ingest it into the RAG knowledge base.
    """

    file_service = FileService()

    # Step 1: Upload File
    result = await file_service.upload_file(file)

    if result["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "File upload failed")
        )

    # Step 2: Initialize Pipeline
    ingestion_pipeline = IngestionPipeline(
        pdf_loader=PDFLoader(),
        text_splitter=TextSplitter(),
        embedding_service=EmbeddingService(),
        vectorstore=ChromaStore(),
    )

    # Step 3: Ingest PDF
    try:
        summary = ingestion_pipeline.ingest_pdf(
            pdf_path=result["file_path"],
            user_id=current_user.id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )

    # Step 4: Return Response
    return UploadResponse(
        filename=result["filename"],
        status=result["status"],
        document_id=summary["document_id"],
        pages_processed=summary["pages_processed"],
        chunks_created=summary["chunks_created"],
    )