from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user import User
from src.utils.auth import decode_access_token
from src.utils.helpers import validate_active_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#-----------CurrentUser--------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()

    if not user:
         raise HTTPException(status_code=401, detail="User not found")

    validate_active_user(user)

    return user

#-----------VerifyUserIsAdmin--------------------
def requiere_admin(current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
