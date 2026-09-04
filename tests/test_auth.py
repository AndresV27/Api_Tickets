def test_login_success(client):
    response = client.post("/auth/login", data={
        "username": "admin@gmail.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    response = client.post("/auth/login", data={
        "username": "admin@gmail.com",
        "password": "admin21323"
    })
    assert response.status_code == 401

def test_login_user_not_found(client):
    response = client.post("/auth/login", data={
        "username": "admin12323@gmail.com",
        "password": "admin123"
    })
    assert response.status_code == 401
    
    