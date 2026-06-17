"""
SQLAlchemy User model for authentication and authorization.

Supports three roles: customer, support, admin.
"""
import enum
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Enum

from app.database.database import Base


class UserRole(str, enum.Enum):
    """Enumeration of valid user roles."""
    customer = "customer"
    support = "support"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password = Column(
        String,
        nullable=False,
    )

    role = Column(
        Enum(UserRole),
        default=UserRole.customer,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
