"""
FastAPI dependencies for authentication.

Provides the database session dependency and the ``get_current_user``
dependency that validates JWT bearer tokens and resolves the active user.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import TokenError, verify_token
from app.database.database import SessionLocal
from app.models.user import User

# ---------------------------------------------------------------------------
# OAuth2 scheme — ``tokenUrl`` must match the mounted login path
# ---------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ---------------------------------------------------------------------------
# Database session dependency
# ---------------------------------------------------------------------------


def get_db():
    """Yield a SQLAlchemy session and ensure it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Current-user dependency
# ---------------------------------------------------------------------------


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated user from a JWT bearer token.

    Raises:
        HTTPException 401: If the token is missing, expired, or invalid.
        HTTPException 404: If the user referenced by the token no longer exists.
    """
    try:
        payload = verify_token(token)
    except TokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

