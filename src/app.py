from flask import Flask
from .auth import auth_bp, init_jwt, hash_password
from .booking import booking_bp
from .store import init_users
from .config import load_profile_env, get_config

def create_app():
    app = Flask(__name__)
    
    load_profile_env()
    cfg = get_config()

    app.config["JWT_SECRET_KEY"] = cfg["JWT_SECRET_KEY"]

    init_jwt(app)
    init_users(hash_password) 

    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)

    @app.get("/")
    def root():
        return {"status": "ok", "message": "Appointment Booking API"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)