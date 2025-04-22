from pydantic import BaseModel
from datetime import datetime
from app.schemas import Reservation, TicketType
from enum import Enum

class TicketStatus(str, Enum):
    valid = "valid"
    used = "used"
    cancelled = "cancelled"

class TicketCreate(BaseModel):
    reservation_id: int
    ticket_type_id: int
    status: TicketStatus = TicketStatus.valid

class TicketUpdate(BaseModel):
    status: TicketStatus

class Ticket(BaseModel):
    id: int
    reservation: Reservation
    ticket_type: TicketType
    ticket_code: str
    status: TicketStatus

    class Config:
        from_attributes = True
