import pytest
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.database.database import SessionLocal
from app.models.document import Document
from app.services.document_service import extract_document_group
from app.auth.rbac import require_admin
from app.models.user import User

def test_extract_document_group():
    assert extract_document_group("Refund_Policy.pdf") == "refund_policy"
    assert extract_document_group("Refund_Policy_New.pdf") == "refund_policy"
    assert extract_document_group("refund_policy_v2.pdf") == "refund_policy"
    assert extract_document_group("something_else.pdf") == "something_else"
    assert extract_document_group("terms_and_conditions_v10.pdf") == "terms_and_conditions"

def test_document_lifecycle(client: TestClient):
    import uuid
    # Override admin dependency
    from app.main import app
    app.dependency_overrides[require_admin] = lambda: User(id=1, email="admin@test.com", username="admin", role="admin")

    with patch('app.services.file_service.FileService.upload_file') as mock_upload, \
         patch('app.pipelines.ingestion_pipeline.IngestionPipeline.ingest_pdf') as mock_ingest:
        
        async def mock_upload_coro(file):
            return {"status": "completed", "filename": file.filename, "file_path": f"/tmp/{file.filename}"}
        mock_upload.side_effect = mock_upload_coro
        mock_ingest.return_value = {"document_id": "test", "pages_processed": 1, "chunks_created": 5}

        # Create dummy pdf file
        test_file_path = "test_lifecycle.pdf"
        with open(test_file_path, "wb") as f:
            f.write(b"%PDF-1.4 dummy content")

        unique_id = uuid.uuid4().hex[:8]
        filename_v1 = f"{unique_id}_Refund_Policy.pdf"
        filename_v2 = f"{unique_id}_Refund_Policy_New.pdf"
        expected_group = f"{unique_id}_refund_policy"

        try:
            # 1. Upload v1
            with open(test_file_path, "rb") as f:
                response1 = client.post(
                    "/api/documents/upload",
                    files={"file": (filename_v1, f, "application/pdf")},
                    data={"document_type": "policy", "version": ""}
                )
            
            assert response1.status_code == 200
            doc1 = response1.json()
            assert doc1["document_group"] == expected_group
            assert doc1["version"] == "v1"
            assert doc1["status"] == "active"
            doc1_id = doc1["id"]

            # 2. Upload v2 (same group)
            with open(test_file_path, "rb") as f:
                response2 = client.post(
                    "/api/documents/upload",
                    files={"file": (filename_v2, f, "application/pdf")},
                    data={"document_type": "policy", "version": ""}
                )
            
            assert response2.status_code == 200
            doc2 = response2.json()
            assert doc2["document_group"] == expected_group
            assert doc2["version"] == "v2"
            assert doc2["status"] == "active"
            assert doc2["previous_version_id"] == doc1_id
            doc2_id = doc2["id"]

            # 3. Check history
            history_response = client.get(f"/api/documents/{doc2_id}/history")
            assert history_response.status_code == 200
            history = history_response.json()
            assert len(history) == 2
            
            # doc1 should now be archived
            db = SessionLocal()
            doc1_db = db.query(Document).filter(Document.id == doc1_id).first()
            assert doc1_db.status == "archived"

            # 4. Check audit log
            audit_response = client.get(f"/api/documents/{doc2_id}/audit")
            assert audit_response.status_code == 200
            audits = audit_response.json()
            assert len(audits) >= 2
            actions = [a["action"] for a in audits]
            assert "UPLOAD" in actions
            assert "ACTIVATE" in actions

            # 5. Rollback
            rollback_response = client.post(f"/api/documents/{doc2_id}/rollback", json={"target_version_id": doc1_id})
            assert rollback_response.status_code == 200
            
            db.expire_all()
            doc1_db = db.query(Document).filter(Document.id == doc1_id).first()
            assert doc1_db.status == "active"
            doc2_db = db.query(Document).filter(Document.id == doc2_id).first()
            assert doc2_db.status == "archived"

            db.close()
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
            if require_admin in app.dependency_overrides:
                del app.dependency_overrides[require_admin]
