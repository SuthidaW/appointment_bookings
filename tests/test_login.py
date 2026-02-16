def test_login_success_admin(client):
    resp = client.post("/login", json={"username": "admin", "password": "admin1234"})
    assert resp.status_code == 200
    assert "access_token" in resp.get_json()

def test_login_success_non_admin(client):
    resp = client.post("/login", json={"username": "suthida", "password": "suthida1234"})
    assert resp.status_code == 200
    assert "access_token" in resp.get_json()

def test_login_fail_wrong_password(client):
    resp = client.post("/login", json={"username": "suthida", "password": "wrong"})
    assert resp.status_code == 401
    assert "error" in resp.get_json()

def test_login_fail_unknown_user(client):
    resp = client.post("/login", json={"username": "ghost", "password": "x"})
    assert resp.status_code == 401