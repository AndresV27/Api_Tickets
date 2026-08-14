from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable= False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    tickets = relationship("Ticket", foreign_keys= "Ticket.user_id",back_populates="owner")
    role = relationship("Role", back_populates="users")
    assigned_tickets = relationship("Ticket", foreign_keys="Ticket.assigned_to", back_populates="assigned")
    comments = relationship("Comment", back_populates="owner")
    ticket_history = relationship("TicketHistory", back_populates="changed_by_user")