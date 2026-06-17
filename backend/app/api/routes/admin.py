from fastapi import APIRouter, Depends

from app.auth.rbac import require_admin
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/")
async def admin_dashboard(
    current_user: User = Depends(require_admin)
):
    """
    Foundational admin route.
    Only accessible by users with the 'admin' role.
    """
    return {"message": "Admin area", "user": current_user.username}
