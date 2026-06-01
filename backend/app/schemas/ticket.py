from pydantic import BaseModel
from typing import Optional

# Validation schemas for support tickets
# TODO: Align fields with actual DB/Databricks table schema.

class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Optional[str] = "low"
