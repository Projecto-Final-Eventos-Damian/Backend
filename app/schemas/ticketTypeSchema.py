from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from app import schemas

class TicketTypeCreate(BaseModel):
    event_id: int
    name: str
    description: Optional[str] = None
    price: condecimal(max_digits=10, decimal_places=2)

class TicketTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: condecimal(max_digits=10, decimal_places=2)

class TicketType(BaseModel):
    id: int
    event_id: int
    name: str
    description: Optional[str]
    price: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True
