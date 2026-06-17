"""
Security utilities for password hashing and JWT token management.

Uses passlib[bcrypt] for password hashing and python-jose for JWT operations.
All configuration is read from environment variables with sensible defaults
for local development.
"""
import os
from datetime import datetime, timedelta, timezone

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Args:
        password: The plaintext password to hash.

    Returns:
        The bcrypt-hashed password string.
    """
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash.

    Args:
        plain_password: The plaintext password provided by the user.
        hashed_password: The stored bcrypt hash to verify against.

    Returns:
        True if the password matches, False otherwise.
    """
    return _pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# JWT configuration — read from environment with development defaults
# ---------------------------------------------------------------------------

JWT_SECRET_KEY: str = os.getenv(
    "JWT_SECRET_KEY",
    "dev-secret-key-change-in-production",
)
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"),
)


# ---------------------------------------------------------------------------
# Token generation
# ---------------------------------------------------------------------------


def create_access_token(data: dict) -> str:
    """Create a signed JWT access token.

    The token embeds the supplied *data* (which should contain ``sub``,
    ``email``, and ``role`` claims) plus an ``exp`` (expiration) claim
    derived from ``ACCESS_TOKEN_EXPIRE_MINUTES``.

    Args:
        data: A dict of claims to encode into the JWT.  Expected keys:
              ``sub`` (user id), ``email``, ``role``.

    Returns:
        The encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# ---------------------------------------------------------------------------
# Token validation
# ---------------------------------------------------------------------------


class TokenError(Exception):
    """Raised when a JWT token cannot be validated."""

    def __init__(self, detail: str = "Could not validate token") -> None:
        self.detail = detail
        super().__init__(self.detail)


def verify_token(token: str) -> dict:
    """Decode and validate a JWT access token.

    Args:
        token: The raw JWT string.

    Returns:
        The decoded payload dictionary.

    Raises:
        TokenError: If the token is expired, invalid, or malformed.
    """
    try:
        payload: dict = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        # Ensure mandatory claims are present
        if payload.get("sub") is None:
            raise TokenError("Token missing 'sub' claim")
        return payload
    except ExpiredSignatureError:
        raise TokenError("Token has expired")
    except JWTError:
        raise TokenError("Invalid or malformed token")
