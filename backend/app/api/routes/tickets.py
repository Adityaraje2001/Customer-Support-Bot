from fastapi import APIRouter, HTTPException, Depends

from app.auth.rbac import require_customer, require_support
from app.models.user import User, UserRole
from app.schemas.ticket import (
    TicketResponse,
    UpdateTicketStatusRequest
)

from app.services.ticket_service import TicketService


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

# =====================================================
# Shared Services
# =====================================================

ticket_service = TicketService()

# =====================================================
# Ticket Endpoints
# =====================================================

@router.get("/my", response_model=list[TicketResponse])
async def get_my_tickets(
    current_user: User = Depends(require_customer)
):
    """Get all tickets for the authenticated customer."""
    return ticket_service.get_user_tickets(current_user.id)  # type: ignore


@router.get("/open", response_model=list[TicketResponse])
async def get_open_tickets(
    current_user: User = Depends(require_support)
):
    """List open tickets (support/admin only)."""
    return ticket_service.list_open_tickets()


@router.get("/resolved", response_model=list[TicketResponse])
async def get_resolved_tickets(
    current_user: User = Depends(require_support)
):
    """List resolved tickets (support/admin only)."""
    return ticket_service.list_resolved_tickets()


@router.get("/", response_model=list[TicketResponse])
async def get_all_tickets(
    current_user: User = Depends(require_support)
):
    """List all tickets (support/admin only)."""
    return ticket_service.get_all_tickets()


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(require_customer)
):
    """Get a specific ticket. Customers can only view their own."""
    ticket = ticket_service.get_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if current_user.role == UserRole.customer and ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted to view this ticket")

    return ticket


@router.patch("/{ticket_id}/resolve", response_model=TicketResponse)
async def resolve_ticket(
    ticket_id: int,
    current_user: User = Depends(require_support)
):
    """Resolve a ticket (support/admin only)."""
    ticket = ticket_service.update_ticket_status(ticket_id, "resolved")
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}/close", response_model=TicketResponse)
async def close_ticket(
    ticket_id: int,
    current_user: User = Depends(require_support)
):
    """Close a ticket (support/admin only)."""
    ticket = ticket_service.update_ticket_status(ticket_id, "closed")
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}/in-progress", response_model=TicketResponse)
async def in_progress_ticket(
    ticket_id: int,
    current_user: User = Depends(require_support)
):
    """Mark a ticket as in-progress (support/admin only)."""
    ticket = ticket_service.update_ticket_status(ticket_id, "in_progress")
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    request: UpdateTicketStatusRequest,
    current_user: User = Depends(require_support)
):
    """Update ticket status manually (support/admin only)."""
    ticket = ticket_service.update_ticket_status(ticket_id, request.status)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket 