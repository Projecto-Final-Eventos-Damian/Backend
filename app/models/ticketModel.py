from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id", ondelete="CASCADE"), nullable=False)
    ticket_type_id = Column(Integer, ForeignKey("ticket_types.id"), nullable=False)
    ticket_code = Column(String(50), unique=True, nullable=False)
    status = Column(Enum("valid", "used", "cancelled", name="ticket_status"), default="valid", nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    reservation = relationship("Reservation", back_populates="tickets")
    ticket_type = relationship("TicketType", back_populates="tickets")
