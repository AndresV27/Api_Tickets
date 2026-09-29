from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime, timezone

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable= False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    ticket_id = Column(Integer,ForeignKey("tickets.id"), nullable= False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner = relationship("User", back_populates="comments")
    ticket = relationship("Ticket", back_populates="comments")
