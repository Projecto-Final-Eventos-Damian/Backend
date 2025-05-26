from pydantic import BaseModel, conint
from datetime import datetime
from app import schemas
from enum import Enum
from .userSchema import User
from .eventSchema import Event
from .ticketSchema import Ticket

class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class ReservationCreate(BaseModel):
    user_id: int
    event_id: int
    status: ReservationStatus = ReservationStatus.pending
    tickets_number: conint(ge=1)

class ReservationUpdate(BaseModel):
    status: ReservationStatus

class Reservation(BaseModel):
    id: int
    user: User
    event: Event
    status: ReservationStatus
    tickets_number: conint(ge=1)
    reserved_at: datetime

    class Config:
        from_attributes = True

class ReservationWithTickets(BaseModel):
    reservation: Reservation
    tickets: list[Ticket]

    class Config:
        from_attributes = True
