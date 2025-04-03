from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    capacity = Column(Integer, nullable=False)
    date_time = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relaciones (opcional si quieres acceder directamente a la categoría y organizador)
    category = relationship("Category", back_populates="events")
    organizer = relationship("User", back_populates="events")
