from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.ticket import Ticket
from src.models.user import User

#-----------SearchTickets--------------------
def get_ticket_or_404(ticket_id: int, db: Session)->Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found" )
    return ticket

#-----------SearchUsers--------------------
def get_user_or_404(user_id: int, db: Session)->User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found" )
    return user

#-----------ValidateUsers--------------------
def validate_active_user(user: User):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

#-----------VerifyTicketOwner--------------------
def verify_ticket_owner(ticket: Ticket, current_user: User):
    if ticket.user_id != current_user.id:
       raise HTTPException(status_code=403, detail="Not authorized to access this ticket")
    