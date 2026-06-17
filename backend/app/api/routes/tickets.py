'''This for GET    /tickets
GET    /tickets/{ticket_id}
PATCH  /tickets/{ticket_id}
GET    /tickets/open'''
from fastapi import APIRouter, HTTPException

from app.schemas.ticket import (
    TicketResponse,
    UpdateTicketStatusRequest
)

from app.services.ticket_service import TicketService


router = APIRouter()

# =====================================================
# Shared Services
# =====================================================

ticket_service = TicketService()

# =====================================================
# Ticket Endpoints
# =====================================================

@router.get(
    "/",
    response_model=list[TicketResponse]
)
async def get_all_tickets():
    return ticket_service.get_all_tickets()



@router.get("/{ticket_id}")
async def get_ticket(
    ticket_id: int
):
    ticket = ticket_service.get_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket   

@router.patch("/{ticket_id}")
async def update_ticket(
    ticket_id: int,
    request: UpdateTicketStatusRequest
):
    ticket = ticket_service.update_ticket_status(ticket_id, request.status)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket   

@router.get("/open")
async def get_open_tickets():
    return ticket_service.list_open_tickets() 