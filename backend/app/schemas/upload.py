from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    status: str
    document_id: str
    pages_processed: int
    chunks_created: int