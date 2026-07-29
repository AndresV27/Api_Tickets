from fastapi import APIRouter, Depends
from src.models import comment
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user import User
from src.models.comment import Comment
from src.utils.dependencies import get_current_user
from src.utils.helpers import get_ticket_or_404
from src.schemas.comment_schema import CommentBase, CommentCreate, CommentResponse

comment_router = APIRouter(prefix="/comments", tags=["Comments"])

#-----------CreateComment--------------------
@comment_router.post("/{ticket_id}/comments", response_model=CommentResponse)
def create_comment(ticket_id: int, comment: CommentCreate, db: Session= Depends(get_db), current_user: User= Depends(get_current_user)):
    get_ticket_or_404(ticket_id, db)
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




