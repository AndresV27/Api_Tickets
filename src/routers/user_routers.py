from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models.user import User
from src.schemas.user_schema import UserResponse , UserCreate, UserUpdate, UserRolerUpdate
from src.utils.helpers import get_user_or_404
from src.utils.auth import hash_password
from src.utils.dependencies import get_current_user, requiere_admin
user_router = APIRouter(prefix="/users", tags=["Users"])

#-----------CreateUsers--------------------
@user_router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name = user.name,
        email = user.email,
        password = hash_password(user.password),
        role_id = 2
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#-----------Users-------------------------
@user_router.get("/", response_model=list[UserResponse])
def get_users(
    is_active: bool | None= None,
    page: int =1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(requiere_admin)):
   
    query = db.query(User)

    if is_active is not None:
       query = query.filter(User.is_active == is_active)

    return query.offset((page -1) * limit).limit(limit).all()  

#-----------GetUser--------------------
@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user_or_404(user_id, db)
    if current_user.role_id != 1 and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

#-----------UpdateUser--------------------
@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user_or_404(user_id, db)
    if current_user.role_id != 1 and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user   

#-----------DeactivateUser--------------------
@user_router.patch("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(requiere_admin)):
    user = get_user_or_404(user_id, db)
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

#-----------AssingRoleToUser--------------------
@user_router.patch("/{user_id}/role", response_model= UserResponse)
def assing_role(user_id: int, user_role: UserRolerUpdate ,db: Session = Depends(get_db), current_user: User = Depends(requiere_admin)):
    user = get_user_or_404(user_id, db)
    user.role_id = user_role.role_id
    db.commit()
    db.refresh(user)
    return user
