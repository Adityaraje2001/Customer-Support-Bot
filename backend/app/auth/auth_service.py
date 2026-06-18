"""
Authentication service layer.

Handles user authentication workflows: credential verification and
JWT token issuance.  Operates against the database via SQLAlchemy sessions.
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.auth.security import verify_password, create_access_token


def authenticate_user(
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    """Look up a user by email and verify their password.

    Args:
        email: The email address supplied at login.
        password: The plaintext password supplied at login.
        db: An active SQLAlchemy database session.

    Returns:
        The ``User`` instance if credentials are valid, otherwise ``None``.
    """
    user: Optional[User] = (
        db.query(User).filter(User.email == email).first()
    )
    if user is None:
        return None
    if not verify_password(password, str(user.hashed_password)):
        return None
    return user


def login(
    email: str,
    password: str,
    db: Session,
) -> Optional[dict]:
    """Authenticate a user and return a bearer token response.

    Args:
        email: The email address supplied at login.
        password: The plaintext password supplied at login.
        db: An active SQLAlchemy database session.

    Returns:
        A dict of the form ``{"access_token": "...", "token_type": "bearer"}``
        if authentication succeeds, otherwise ``None``.
    """
    user = authenticate_user(email, password, db)
    if user is None:
        return None

    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
    }
    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
