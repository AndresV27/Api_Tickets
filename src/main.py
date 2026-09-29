from fastapi import FastAPI
from src.models import comment, role, ticket, user, ticket_history
from src.database.db import engine, SessionLocal
from src.models import role, user
from src.models.role import Role
from src.models.user import User
from src.routers.user_routers import user_router
from src.routers.auth_routers import auth_router
from src.routers.ticket_routers import ticket_router
from src.routers.comment_routers import comment_router
from src.utils.auth import hash_password
from contextlib import asynccontextmanager


import os

comment.Base.metadata.create_all(bind=engine)
role.Base.metadata.create_all(bind=engine)
ticket.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
ticket_history.Base.metadata.create_all(bind=engine)

#-----------CreateDefaultRoles--------------------
def create_default_roles():
    db = SessionLocal()
    try:
        if not db.query(Role).first():
            roles = [
                Role(name= "admin"),
                Role(name= "user")
            ]
            db.add_all(roles)
            db.commit()
    finally:
        db.close()    

#-----------CreateDefaultAdmin--------------------
def create_default_admin():
    db = SessionLocal()
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        if not db.query(User).filter(User.email == admin_email).first():
            admin = User(
                name = "Admin",
                email = admin_email,
                password = hash_password(admin_password),
                role_id = 1,
                is_active = True
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()        

@asynccontextmanager
async def startup(app: FastAPI):
    create_default_roles()
    create_default_admin()
    yield       

app = FastAPI(title="Tickets API",  lifespan= startup)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(comment_router)


@app.get("/")
def root():
    return {"message": "Welcome to Tickets API"}