import pytest 
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def user_token(client):
    login = client.post("/auth/login", data={
        "username": "admin@gmail.com",
        "password": "admin123"
    })
    return login.json()["access_token"]

@pytest.fixture
def auth_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}