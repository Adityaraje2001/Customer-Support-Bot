"""
Purpose:
Test the `/upload` endpoint for PDF document ingestion.

Mocks required:
- `app.api.routes.upload.FileService`: Mock file saving to prevent local disk writes.
- `app.api.routes.upload.IngestionPipeline`: Mock the entire pipeline to prevent PDF parsing, chunking, embedding generation, and ChromaDB writes.

Execution:
Run `pytest backend/tests/test_upload_api.py -v`
"""

import pytest
from unittest.mock import AsyncMock, patch


def test_upload_success(client, mocker):
    # Arrange
    mock_file_service_cls = mocker.patch("app.api.routes.upload.FileService")
    mock_file_service = mock_file_service_cls.return_value
    mock_file_service.upload_file = AsyncMock(return_value={
        "status": "completed",
        "file_path": "/tmp/test.pdf",
        "filename": "test.pdf"
    })

    mock_pipeline_cls = mocker.patch("app.api.routes.upload.IngestionPipeline")
    mock_pipeline = mock_pipeline_cls.return_value
    mock_pipeline.ingest_pdf.return_value = {
        "document_id": "doc-123",
        "pages_processed": 5,
        "chunks_created": 20
    }

    # Since FileService, IngestionPipeline use other components internally 
    # we patch them out at the route level to prevent instantiating real ones.
    mocker.patch("app.api.routes.upload.PDFLoader")
    mocker.patch("app.api.routes.upload.TextSplitter")
    mocker.patch("app.api.routes.upload.EmbeddingService")
    mocker.patch("app.api.routes.upload.ChromaStore")

    # Act
    with open(__file__, "rb") as f:
        # Send current file as dummy PDF for the test client
        response = client.post("/api/upload/", files={"file": ("test.pdf", f, "application/pdf")})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["status"] == "completed"
    assert data["document_id"] == "doc-123"
    assert data["pages_processed"] == 5
    assert data["chunks_created"] == 20

    mock_file_service.upload_file.assert_called_once()
    mock_pipeline.ingest_pdf.assert_called_once_with(pdf_path="/tmp/test.pdf")


def test_upload_file_service_error(client, mocker):
    # Arrange
    mock_file_service_cls = mocker.patch("app.api.routes.upload.FileService")
    mock_file_service = mock_file_service_cls.return_value
    mock_file_service.upload_file = AsyncMock(return_value={
        "status": "failed",
        "error": "Invalid file format"
    })

    # Act
    with open(__file__, "rb") as f:
        response = client.post("/api/upload/", files={"file": ("test.txt", f, "text/plain")})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file format"


def test_upload_ingestion_error(client, mocker):
    # Arrange
    mock_file_service_cls = mocker.patch("app.api.routes.upload.FileService")
    mock_file_service = mock_file_service_cls.return_value
    mock_file_service.upload_file = AsyncMock(return_value={
        "status": "completed",
        "file_path": "/tmp/test.pdf",
        "filename": "test.pdf"
    })

    mock_pipeline_cls = mocker.patch("app.api.routes.upload.IngestionPipeline")
    mock_pipeline = mock_pipeline_cls.return_value
    mock_pipeline.ingest_pdf.side_effect = Exception("ChromaDB connection failed")

    mocker.patch("app.api.routes.upload.PDFLoader")
    mocker.patch("app.api.routes.upload.TextSplitter")
    mocker.patch("app.api.routes.upload.EmbeddingService")
    mocker.patch("app.api.routes.upload.ChromaStore")

    # Act
    with open(__file__, "rb") as f:
        response = client.post("/api/upload/", files={"file": ("test.pdf", f, "application/pdf")})

    # Assert
    assert response.status_code == 500
    assert "ChromaDB connection failed" in response.json()["detail"]
