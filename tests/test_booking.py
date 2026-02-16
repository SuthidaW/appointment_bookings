def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

def login_and_get_token(client, username: str, password: str) -> str:
    resp = client.post("/login", json={"username": username, "password": password})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]

def test_non_admin_can_create_and_see_only_own_bookings(client):
    suthida_token = login_and_get_token(client, "suthida", "suthida1234")

    r_create = client.post("/bookings", headers=auth_header(suthida_token), json={"slot": "10am-11am"})
    assert r_create.status_code == 201
    assert r_create.get_json()["owner"] == "suthida"

    r_list = client.get("/bookings", headers=auth_header(suthida_token))
    assert r_list.status_code == 200
    items = r_list.get_json()
    assert all(b["owner"] == "suthida" for b in items)

def test_admin_can_view_all_bookings(client):
    admin_token = login_and_get_token(client, "admin", "admin1234")
    suthida_token = login_and_get_token(client, "suthida", "suthida1234")

    client.post("/bookings", headers=auth_header(suthida_token), json={"slot": "10am-11am"})
    client.post("/bookings", headers=auth_header(admin_token), json={"slot": "1pm-2pm"})

    r_list = client.get("/bookings", headers=auth_header(admin_token))
    assert r_list.status_code == 200
    owners = {b["owner"] for b in r_list.get_json()}
    assert "suthida" in owners
    assert "admin" in owners

def test_non_admin_cannot_delete_other_users_booking(client):
    admin_token = login_and_get_token(client, "admin", "admin1234")
    suthida_token = login_and_get_token(client, "suthida", "suthida1234")

    r_admin = client.post("/bookings", headers=auth_header(admin_token), json={"slot": "1pm-2pm"})
    booking_id = r_admin.get_json()["id"]

    r_del = client.delete(f"/bookings/{booking_id}", headers=auth_header(suthida_token))
    assert r_del.status_code == 403

def test_admin_can_delete_any_booking(client):
    admin_token = login_and_get_token(client, "admin", "admin1234")
    suthida_token = login_and_get_token(client, "suthida", "suthida1234")

    r_suthida = client.post("/bookings", headers=auth_header(suthida_token), json={"slot": "10am-11am"})
    booking_id = r_suthida.get_json()["id"]

    r_del = client.delete(f"/bookings/{booking_id}", headers=auth_header(admin_token))
    assert r_del.status_code == 200
    assert r_del.get_json()["deleted"] == booking_id