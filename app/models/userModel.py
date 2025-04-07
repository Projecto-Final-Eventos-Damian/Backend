from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("user", "organizer", "admin", name="user_roles"), default="user")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    events = relationship("Event", back_populates="organizer")
    ratings = relationship("EventRating", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")