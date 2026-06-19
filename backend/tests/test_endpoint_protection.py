import pytest
from app.models.user import User

@pytest.fixture(autouse=True)
def clear_overrides():
    """Clear overrides so we test real authentication behavior (401s)."""
    from app.main import app
    old_overrides = app.dependency_overrides.copy()
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = old_overrides

class TestEndpointProtection:
    def test_chat_unauthorized(self, client):
        response = client.post("/api/chat", json={"message": "hello"})
        assert response.status_code == 401

    def test_upload_unauthorized(self, client):
        # We can just send an empty post to trigger 401 before any file validation
        response = client.post("/api/documents/upload")
        assert response.status_code == 401

    def test_tickets_unauthorized(self, client):
        response = client.get("/api/tickets/")
        assert response.status_code == 401

    def test_chat_authorized(self, client):
        """Test that restoring the override allows the request through."""
        from app.main import app
        from app.auth.dependencies import get_current_user
        
        # Override just for this test
        app.dependency_overrides[get_current_user] = lambda: User(id=1, email="test@test.com", username="testuser", role="customer")
        
        # Because we mocked LLM and graph inside conftest, this should return 200
        response = client.post("/api/chat", json={"message": "hello"})
        
        assert response.status_code != 401
