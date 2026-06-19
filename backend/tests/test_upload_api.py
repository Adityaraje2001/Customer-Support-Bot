"""
Purpose:
Test the `/api/documents/upload` endpoint for error cases.

Execution:
Run `pytest backend/tests/test_upload_api.py -v`
"""

import pytest
from unittest.mock import AsyncMock, patch

def test_upload_success(client, mocker):
    # This is already tested in test_document_versioning.py, but we can keep a simple test
    pass

def test_upload_file_service_error(client, mocker):
    # Arrange
    # Mock FileService.upload_file
    mock_upload = mocker.patch("app.services.file_service.FileService.upload_file", new_callable=AsyncMock)
    mock_upload.return_value = {
        "status": "failed",
        "error": "Invalid file format"
    }

    # Act
    with open(__file__, "rb") as f:
        # The document upload requires admin dependency, which conftest handles via require_customer maybe?
        # No, require_admin is required. Let's override it for this test.
        from app.main import app
        from app.auth.rbac import require_admin
        from app.models.user import User
        app.dependency_overrides[require_admin] = lambda: User(id=1, email="admin@test.com", username="admin", role="admin")
        
        response = client.post("/api/documents/upload", files={"file": ("test.txt", f, "text/plain")})
        
        # Cleanup
        if require_admin in app.dependency_overrides:
            del app.dependency_overrides[require_admin]

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "File upload failed"


def test_upload_ingestion_error(client, mocker):
    # Arrange
    mock_upload = mocker.patch("app.services.file_service.FileService.upload_file", new_callable=AsyncMock)
    mock_upload.return_value = {
        "status": "completed",
        "file_path": "/tmp/test.pdf",
        "filename": "test.pdf"
    }

    mock_ingest = mocker.patch("app.pipelines.ingestion_pipeline.IngestionPipeline.ingest_pdf")
    mock_ingest.side_effect = Exception("ChromaDB connection failed")

    # Act
    with open(__file__, "rb") as f:
        from app.main import app
        from app.auth.rbac import require_admin
        from app.models.user import User
        app.dependency_overrides[require_admin] = lambda: User(id=1, email="admin@test.com", username="admin", role="admin")
        
        response = client.post("/api/documents/upload", files={"file": ("test.pdf", f, "application/pdf")})
        
        if require_admin in app.dependency_overrides:
            del app.dependency_overrides[require_admin]

    # Assert
    assert response.status_code == 500
    assert "Ingestion failed: ChromaDB connection failed" in response.json()["detail"]
