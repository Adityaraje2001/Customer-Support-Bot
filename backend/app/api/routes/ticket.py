from fastapi import APIRouter
from app.schemas.ticket import TicketCreate

# TODO: Implement endpoint for support ticket creation and management

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/")
async def create_ticket(ticket: TicketCreate):
    return {"status": "created", "title": ticket.title}
