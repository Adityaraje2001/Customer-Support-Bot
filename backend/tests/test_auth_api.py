"""
Tests for the /api/auth endpoints.

Covers registration, login (OAuth2 form data), /me (JWT-protected),
and edge cases for validation, duplicates, and invalid tokens.
"""
import pytest
from app.models.user import User
from app.database.database import SessionLocal
from app.auth.security import create_access_token

@pytest.fixture(autouse=True)
def clear_overrides():
    from app.main import app
    old_overrides = app.dependency_overrides.copy()
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = old_overrides
@pytest.fixture(autouse=True)
def clean_users():
    """Ensure a clean users table for every test."""
    db = SessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()


# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------


def _register(client, email="user@test.com", username="aditya", password="password123"):
    """Register a user and return the response."""
    return client.post("/api/auth/register", json={
        "email": email,
        "username": username,
        "password": password,
    })


def _login(client, email="user@test.com", password="password123"):
    """Log in via OAuth2 form data and return the response."""
    return client.post("/api/auth/login", data={
        "username": email,       # OAuth2 spec: email goes in the 'username' field
        "password": password,
    })


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# -----------------------------------------------------------------------
# Registration
# -----------------------------------------------------------------------


class TestRegister:
    def test_register_success(self, client):
        response = _register(client)
        assert response.status_code == 201
        assert response.json() == {"message": "User registered successfully"}

    def test_register_duplicate_email(self, client):
        _register(client)
        response = _register(client, username="other")
        assert response.status_code == 400
        assert "Email already" in response.json()["detail"]

    def test_register_duplicate_username(self, client):
        _register(client)
        response = _register(client, email="other@test.com")
        assert response.status_code == 400
        assert "Username already" in response.json()["detail"]

    def test_register_short_password(self, client):
        """Passwords shorter than 8 chars should be rejected by Pydantic validation."""
        response = _register(client, password="short")
        assert response.status_code == 422

    def test_register_invalid_email(self, client):
        """Malformed email addresses should be rejected by Pydantic validation."""
        response = _register(client, email="not-an-email")
        assert response.status_code == 422

    def test_register_short_username(self, client):
        """Usernames shorter than 3 chars should be rejected by Pydantic validation."""
        response = _register(client, username="ab")
        assert response.status_code == 422

    def test_register_default_role_is_customer(self, client):
        """New users should be assigned the 'customer' role by default."""
        _register(client)
        login_res = _login(client)
        token = login_res.json()["access_token"]
        me_res = client.get("/api/auth/me", headers=_auth_header(token))
        assert me_res.json()["role"] == "customer"


# -----------------------------------------------------------------------
# Login
# -----------------------------------------------------------------------


class TestLogin:
    def test_login_success(self, client):
        _register(client)
        response = _login(client)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        _register(client)
        response = _login(client, password="wrongpassword")
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = _login(client)
        assert response.status_code == 401

    def test_login_missing_fields(self, client):
        """Missing form fields should return 422."""
        response = client.post("/api/auth/login", data={})
        assert response.status_code == 422


# -----------------------------------------------------------------------
# Token validation & /me
# -----------------------------------------------------------------------


class TestMe:
    def test_me_success(self, client):
        _register(client)
        login_res = _login(client)
        token = login_res.json()["access_token"]

        response = client.get("/api/auth/me", headers=_auth_header(token))
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "user@test.com"
        assert data["username"] == "aditya"
        assert data["role"] == "customer"
        assert "id" in data
        assert "created_at" in data

    def test_me_invalid_token(self, client):
        response = client.get("/api/auth/me", headers=_auth_header("invalidtoken"))
        assert response.status_code == 401

    def test_me_no_auth_header(self, client):
        """Requests without an Authorization header should be rejected."""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_me_expired_token(self, client):
        """Tokens with a past expiration should be rejected."""
        from datetime import datetime, timedelta, timezone
        from jose import jwt
        from app.auth.security import JWT_SECRET_KEY, JWT_ALGORITHM

        expired_payload = {
            "sub": "1",
            "email": "user@test.com",
            "role": "customer",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        }
        expired_token = jwt.encode(expired_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        response = client.get("/api/auth/me", headers=_auth_header(expired_token))
        assert response.status_code == 401

    def test_me_token_missing_sub_claim(self, client):
        """A token without a 'sub' claim should be rejected."""
        from jose import jwt
        from app.auth.security import JWT_SECRET_KEY, JWT_ALGORITHM
        from datetime import datetime, timedelta, timezone

        bad_payload = {
            "email": "user@test.com",
            "role": "customer",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        bad_token = jwt.encode(bad_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        response = client.get("/api/auth/me", headers=_auth_header(bad_token))
        assert response.status_code == 401
