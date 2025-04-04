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
    start_date_time: datetime
    end_date_time: datetime
    location: str
    image_url: Optional[HttpUrl] = None

class Event(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: schemas.Category
    organizer: schemas.User
    capacity: int
    start_date_time: datetime
    end_date_time: datetime
    location: str
    image_url: Optional[HttpUrl] = None

    class Config:
        from_attributes = True
