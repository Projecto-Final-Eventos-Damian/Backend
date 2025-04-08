from pydantic import BaseModel, condecimal
from datetime import datetime
from app import schemas
from enum import Enum

class TicketStatus(str, Enum):
    valid = "valid"
    used = "used"
    cancelled = "cancelled"

class TicketCreate(BaseModel):
    reservation_id: int
    price: condecimal(max_digits=10, decimal_places=2)
    status: TicketStatus = TicketStatus.valid

class TicketUpdate(BaseModel):
    status: TicketStatus

class Ticket(BaseModel):
    id: int
    reservation: schemas.Reservation
    ticket_code: str
    price: condecimal(max_digits=10, decimal_places=2)
    status: TicketStatus

    class Config:
        from_attributes = True
