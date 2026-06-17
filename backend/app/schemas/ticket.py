from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: int
    session_id: str
    question: str
    status: str

    class Config:
        from_attributes = True


class UpdateTicketStatusRequest(BaseModel):
    status: str