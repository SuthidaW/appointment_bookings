users = {}     # users[username] = { username, password_hash, is_admin }
bookings = {}  # bookings[id] = { id, owner, slot }


INIT_USERS = [
    {"username": "admin", "password": "admin1234", "is_admin": True},
    {"username": "suthida", "password": "suthida1234", "is_admin": False},
    {"username": "test", "password": "test1234", "is_admin": False},

]


def init_users(hash_password_fn):

    for u in INIT_USERS:
        users[u["username"]] = {
            "username": u["username"],
            "password_hash": hash_password_fn(u["password"]),
            "is_admin": u["is_admin"],
        }
