"""
Pydantic schemas for user authentication.

Includes request/response models for user creation, login, and API responses.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRoleEnum(str, Enum):
    """Mirror of the SQLAlchemy UserRole enum for schema validation."""
    customer = "customer"
    support = "support"
    admin = "admin"


class UserCreate(BaseModel):
    """Schema for user registration requests."""
    email: EmailStr
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username (3-50 characters)",
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
    )
    role: UserRoleEnum = Field(
        default=UserRoleEnum.customer,
        description="User role (defaults to customer)",
    )


class UserLogin(BaseModel):
    """Schema for JSON-based user login requests.

    Note: The primary /auth/login endpoint uses OAuth2PasswordRequestForm
    (form data) for Swagger compatibility. This schema is retained for
    programmatic JSON login use cases.
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for bearer token responses returned by the login endpoint."""
    access_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    """Schema for successful registration responses."""
    message: str


class UserResponse(BaseModel):
    """Schema for user data returned in API responses.

    Excludes sensitive fields like hashed_password.
    """
    id: int
    email: str
    username: str
    role: UserRoleEnum
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
