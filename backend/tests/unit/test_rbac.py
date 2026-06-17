import pytest
from app.models.user import User, UserRole
from app.auth.rbac import require_customer, require_support, require_admin
from fastapi import HTTPException

def test_require_customer_success():
    user = User(id=1, email="c@test.com", username="c", role=UserRole.customer)
    result = require_customer(current_user=user)
    assert result == user

def test_require_support_success():
    user = User(id=1, email="s@test.com", username="s", role=UserRole.support)
    result = require_support(current_user=user)
    assert result == user

def test_require_support_admin_success():
    user = User(id=1, email="a@test.com", username="a", role=UserRole.admin)
    result = require_support(current_user=user)
    assert result == user

def test_require_support_failure():
    user = User(id=1, email="c@test.com", username="c", role=UserRole.customer)
    with pytest.raises(HTTPException) as exc:
        require_support(current_user=user)
    assert exc.value.status_code == 403

def test_require_admin_success():
    user = User(id=1, email="a@test.com", username="a", role=UserRole.admin)
    result = require_admin(current_user=user)
    assert result == user

def test_require_admin_failure_customer():
    user = User(id=1, email="c@test.com", username="c", role=UserRole.customer)
    with pytest.raises(HTTPException) as exc:
        require_admin(current_user=user)
    assert exc.value.status_code == 403

def test_require_admin_failure_support():
    user = User(id=1, email="s@test.com", username="s", role=UserRole.support)
    with pytest.raises(HTTPException) as exc:
        require_admin(current_user=user)
    assert exc.value.status_code == 403
