from fastapi import Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.models.user import User, UserRole

def require_customer(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that requires the user to be authenticated.
    Since 'customer' is the base role, all authenticated users (customer, support, admin)
    can access these endpoints.
    """
    return current_user

def require_support(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that requires the user to have 'support' or 'admin' role.
    """
    if current_user.role not in [UserRole.support, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return current_user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that requires the user to have 'admin' role.
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return current_user
