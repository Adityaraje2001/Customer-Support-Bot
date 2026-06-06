'''This is health api'''


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class HealthCheckResponse(BaseModel):
    status: str
    version: str


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return HealthCheckResponse(status="ok", version="0.1.0")
