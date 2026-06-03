from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime, timezone

class Ticket(Base):
     __tablename__ = "tickets"
     
     id = Column(Integer, primary_key=True, index=True)
     title = Column(String, nullable= False)
     description = Column(String, nullable=False)
     status = Column(String, nullable=False)
     priority = Column(String, nullable= False)
     created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
     assigned_to = Column(Integer, ForeignKey("users.id"), nullable= True)
     owner = relationship("User",foreign_keys=[user_id], back_populates="tickets")
     assigned = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tickets")
     comments = relationship("Comment", back_populates="ticket")