def test_create_ticket_success(client, auth_headers):
    response = client.post("/tickets",
        json={"title": "Test ticket", "description": "Test description", "priority":"low"},
        headers=auth_headers
    )
    assert response.status_code == 200