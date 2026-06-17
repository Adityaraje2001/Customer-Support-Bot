'''This is router file for API'''


from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router
from app.api.routes.upload import router as upload_router
from app.api.routes.tickets import router as tickets_router

router = APIRouter()

router.include_router(health_router)
router.include_router(chat_router)
router.include_router(upload_router)
router.include_router(tickets_router)