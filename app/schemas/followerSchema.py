from pydantic import BaseModel
from datetime import datetime
from app import schemas

class UserFollowerCreate(BaseModel):
    user_id: int
    organizer_id: int

class UserFollower(BaseModel):
    id: int
    user: schemas.User
    organizer: schemas.User
    followed_at: datetime

    class Config:
        from_attributes = True