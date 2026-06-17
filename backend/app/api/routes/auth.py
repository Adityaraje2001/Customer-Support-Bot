"""
Authentication API routes.

Provides user registration, login (OAuth2-compatible), and current-user
retrieval endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth_service import login
from app.auth.dependencies import get_db, get_current_user
from app.auth.security import hash_password
from app.models.user import User
from app.schemas.auth import (
    RegisterResponse,
    TokenResponse,
    UserCreate,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user.

    Validates email and username uniqueness before creating the account.
    New users default to the ``customer`` role unless specified otherwise.
    """
    # Check email uniqueness
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check username uniqueness
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    new_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )
    db.add(new_user)
    db.commit()

    return RegisterResponse(message="User registered successfully")


@router.post("/login", response_model=TokenResponse)
def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate a user and return a bearer token.

    Accepts OAuth2-compatible form data (``username`` field carries the
    email address) so that Swagger's *Authorize* button works out of the box.
    """
    token_response = login(
        email=form_data.username,
        password=form_data.password,
        db=db,
    )

    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_response


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user's profile information."""
    return current_user

