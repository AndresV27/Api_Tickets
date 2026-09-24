def test_create_ticket_success(client, auth_headers):
    response = client.post("/tickets",
        json={"title": "Test ticket", "description": "Test description", "priority":"low"},
        headers=auth_headers
    )
    assert response.status_code == 200

def test_create_unauthorized(client):
    response = client.post("/tickets/",
        json={"title": "Test ticket", "description": "Test description", "priority":"low"}
    )
    assert response.status_code == 401

def test_get_tickets_success(client, auth_headers):
    response = client.get("tickets/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_ticket_not_found(client, auth_headers):
    response = client.get("/tickets/9999", headers=auth_headers)
    assert response.status_code == 404

def test_update_ticket_success(client, auth_headers):
    response = client.put("/tickets/1",
        json={"status": "open"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "open"

def test_update_ticket_not_found(client, auth_headers):
    response = client.put("/tickets/9999",
        json={"status": "open"},
        headers=auth_headers
    )
    assert response.status_code == 404