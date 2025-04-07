from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class EventRating(Base):
    __tablename__ = "event_ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="ratings")
    event = relationship("Event", back_populates="ratings")

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='uq_user_event_rating'),)
