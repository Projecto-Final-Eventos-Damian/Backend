from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.userModel import User

class UserFollower(Base):
    __tablename__ = "user_followers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followed_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", foreign_keys=[user_id])
    organizer = relationship("User", foreign_keys=[organizer_id])

    __table_args__ = (UniqueConstraint('user_id', 'organizer_id', name='uq_user_follow'),)