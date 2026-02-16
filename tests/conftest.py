import os
import pytest

from src.app import create_app
from src.store import bookings, init_users
from src.auth import hash_password


@pytest.fixture()
def app():
    # ให้ใช้ config ของ test ไม่ผูกกับ env จริง
    os.environ["APP_ENV"] = "dev"

    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret-key"  # override ให้ predictable

    # reset in-memory store ก่อนแต่ละ test
    init_users(hash_password)
    bookings.clear()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def login_and_get_token(client, username: str, password: str) -> str:
    resp = client.post("/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.get_json()
    return resp.get_json()["access_token"]