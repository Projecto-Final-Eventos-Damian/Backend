from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
from app import schemas

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: int
    organizer_id: int
    capacity: int
    date_time: datetime
    location: str
    image_url: Optional[HttpUrl] = None  # Usa HttpUrl para validar URLs

class Event(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: schemas.Category
    organizer: schemas.User
    capacity: int
    date_time: datetime
    location: str
    image_url: Optional[HttpUrl] = None  # Usa HttpUrl para validar URLs

    class Config:
        from_attributes = True  # Permite la conversión desde un modelo SQLAlchemy