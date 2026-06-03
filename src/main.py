from fastapi import FastAPI
from src.models import comment, role, ticket, user
from src.database.db import engine

comment.Base.metadata.create_all(bind=engine)
role.Base.metadata.create_all(bind=engine)
ticket.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tickets API")

@app.get("/")
def root():
    return {"message": "Welcome to Tickets API"}