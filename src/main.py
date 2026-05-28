from fastapi import FastAPI

app = FastAPI(title="Tickets API")

@app.get("/")
def root():
    return {"message": "Welcome to Tickets API"}