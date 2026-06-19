'''This is router file for API'''


from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router
from app.api.routes.tickets import router as tickets_router
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from app.api.routes.documents import router as documents_router

router = APIRouter()

router.include_router(health_router)
router.include_router(chat_router)
router.include_router(tickets_router)
router.include_router(auth_router)
router.include_router(admin_router)
router.include_router(documents_router)