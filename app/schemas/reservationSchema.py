from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app import schemas
from enum import Enum

class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class ReservationCreate(BaseModel):
    user_id: int
    event_id: int
    status: ReservationStatus = ReservationStatus.pending
    tickets_number: int

class ReservationUpdate(BaseModel):
    status: ReservationStatus
    tickets_number: int

class Reservation(BaseModel):
    id: int
    user: schemas.User
    event: schemas.Event
    status: ReservationStatus
    tickets_number: int

    class Config:
        from_attributes = True
