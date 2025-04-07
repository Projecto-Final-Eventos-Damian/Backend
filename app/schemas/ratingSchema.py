from pydantic import BaseModel, conint
from typing import Optional
from app import schemas

class EventRatingCreate(BaseModel):
    user_id: int
    event_id: int
    rating: conint(ge=1, le=5) # Integer entre 1 y 5
    review: Optional[str] = None

class EventRatingUpdate(BaseModel):
    rating: conint(ge=1, le=5)
    review: Optional[str]

class EventRating(BaseModel):
    id: int
    user: schemas.User
    event: schemas.Event
    rating: conint(ge=1, le=5)
    review: Optional[str]

    class Config:
        from_attributes = True
