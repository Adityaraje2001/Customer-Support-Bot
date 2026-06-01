from fastapi import APIRouter, UploadFile, File

# TODO: Implement file upload and ingestion endpoints for RAG

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "uploaded"}
