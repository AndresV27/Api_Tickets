from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user import User
from src.utils.auth import verify_password, create_access_token
from src.schemas.auth_schema import TokenResponse
from src.utils.helpers import validate_active_user
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login", response_model= TokenResponse)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    validate_active_user(user)
    
    token = create_access_token(data={"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}