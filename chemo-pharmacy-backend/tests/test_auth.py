def test_register_login_and_me(client):
    reg = client.post(
        "/api/auth/register",
        json={"username": "u1", "password": "1234", "fullname": "Legacy Fullname", "role": "General Pharmacist"},
    )
    assert reg.status_code == 200
    assert reg.json()["data"]["full_name"] == "Legacy Fullname"

    login = client.post("/api/auth/login", json={"username": "u1", "password": "1234"})
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["data"]["username"] == "u1"
