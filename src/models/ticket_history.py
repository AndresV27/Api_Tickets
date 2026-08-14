from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime, timezone

class TicketHistory(Base):
    __tablename__  = "ticket_history"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer,ForeignKey("tickets.id"), nullable= False)
    changed_by = Column(Integer,ForeignKey("users.id"),nullable= False)
    previous_status = Column(String, nullable= False)
    new_status = Column(String, nullable= False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ticket = relationship("Ticket", back_populates="history")
    changed_by_user = relationship("User", back_populates="ticket_history")
    
