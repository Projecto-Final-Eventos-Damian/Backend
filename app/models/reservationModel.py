from sqlalchemy import Column, Integer, ForeignKey, Enum, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    status = Column(Enum("pending", "confirmed", "cancelled", name="reservation_status"), default="pending")
    tickets_number = Column(Integer, nullable=False)
    reserved_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    rating_sent = Column(Boolean, default=False)

    user = relationship("User", back_populates="reservations")
    event = relationship("Event", back_populates="reservations")
    tickets = relationship("Ticket", back_populates="reservation", cascade="all, delete-orphan")
