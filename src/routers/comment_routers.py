from fastapi import APIRouter, Depends, HTTPException
from src.models import comment
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user import User
from src.models.comment import Comment
from src.utils.dependencies import get_current_user, requiere_admin
from src.utils.helpers import get_ticket_or_404
from src.schemas.comment_schema import CommentBase, CommentCreate, CommentResponse

comment_router = APIRouter(prefix="/tickets", tags=["Comments"])

#-----------CreateComment--------------------
@comment_router.post("/{ticket_id}/comments", response_model=CommentResponse)
def create_comment(ticket_id: int, comment: CommentCreate, db: Session= Depends(get_db), current_user: User= Depends(requiere_admin)):
    ticket= get_ticket_or_404(ticket_id, db)
    if ticket.assigned_to != current_user.id and ticket.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_comment = Comment(
        content = comment.content,
        user_id = current_user.id,
        ticket_id = ticket_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment

#-----------GetComments--------------------
@comment_router.get("/{ticket_id}/comments", response_model= list[CommentResponse])
def get_comments(ticket_id: int, db: Session= Depends(get_db), current_user: User= Depends(requiere_admin)):
    ticket= get_ticket_or_404(ticket_id, db)
    if ticket.assigned_to != current_user.id and ticket.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized")

    query = db.query(Comment).filter(Comment.ticket_id == ticket_id).all()
    return  query





