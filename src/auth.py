from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from passlib.context import CryptContext
from .store import users
from flask_jwt_extended import get_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_bp = Blueprint("auth", __name__)

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = "CHANGE_ME_TO_SOMETHING_RANDOM"
    JWTManager(app)

def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    return pwd_context.verify(pw, hashed)

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = users.get(username)
    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=username,
        additional_claims={"is_admin": user["is_admin"]}
    )
    return jsonify({"access_token": token})

def require_admin():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"error": "Admin only"}), 403
    return None