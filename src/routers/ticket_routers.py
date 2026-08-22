from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.database.db import get_db
from src.models.ticket import Ticket
from src.schemas.ticket_schema import TicketCreate, TicketUpdate, TicketResponse, TicketStatus, TicketPriority, TicketAssign
from src.utils.helpers import get_ticket_or_404, verify_ticket_owner, get_user_or_404, register_ticket_history
from src.utils.dependencies import get_current_user, requiere_admin
from src.models.user import User

ticket_router = APIRouter(prefix="/tickets", tags=["Tickets"])

#-----------CreateTickets--------------------
@ticket_router.post("/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_ticket = Ticket(**ticket.model_dump(), user_id= current_user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

#-----------GetTickets-------------------------
@ticket_router.get("/", response_model=list[TicketResponse])
def get_tickets(
    status: TicketStatus | None= None,
    priority: TicketPriority | None= None ,
    page: int =1,
    limit: int = 10 ,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
   
   if current_user.role_id == 1:
       query = db.query(Ticket).filter(
           or_(
               Ticket.assigned_to == current_user.id,
               Ticket.assigned_to == None,
               Ticket.user_id == current_user.id
           )
       )
   else:
       query = db.query(Ticket).filter(Ticket.user_id == current_user.id)
   
   if status is not None:
       query = query.filter(Ticket.status == status)

   if priority is not None:
       query = query.filter(Ticket.priority == priority)   

   return query.offset((page -1) * limit).limit(limit).all()   

#-----------GetTicket--------------------
@ticket_router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = get_ticket_or_404(ticket_id, db)

    if current_user.role_id == 1:
       if ticket.assigned_to != current_user.id and ticket.user_id != current_user.id:
           raise HTTPException(status_code=403, detail="Not authorized")
    else: 
        verify_ticket_owner(ticket, current_user)   
    
    return ticket


#-----------UpdateTicket--------------------
@ticket_router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket_data: TicketUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = get_ticket_or_404(ticket_id, db)
    new_status = ticket_data.status

    if current_user.role_id != 1:
       verify_ticket_owner(ticket, current_user)

    if new_status:
        register_ticket_history(ticket, new_status, current_user, db)

    for field, value in ticket_data.model_dump(exclude_unset=True).items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket   

#-----------AssingUserToTicket--------------------
@ticket_router.patch("/{ticket_id}/assign", response_model= TicketResponse)
def assign_ticket(ticket_id: int, ticket_assign: TicketAssign ,db: Session = Depends(get_db), current_user: User = Depends(requiere_admin)):
    assigned_user = get_user_or_404(ticket_assign.assigned_to, db)
    if assigned_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Only admins can be assigned to tickets")
    ticket = get_ticket_or_404(ticket_id, db)
    ticket.assigned_to = ticket_assign.assigned_to
    db.commit()
    db.refresh(ticket)
    return ticket
