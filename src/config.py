import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT_DIR / "profiles"

def load_profile_env() -> str:
    """
    load profiles/<APP_ENV>/.env
    """
    env = os.getenv("APP_ENV") or "dev"
    env_file = PROFILES_DIR / env / ".env"

    if env_file.exists():
        load_dotenv(env_file, override=True)

    return env

def get_config() -> dict:
    return {
        "APP_ENV": os.getenv("APP_ENV", "dev"),
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "xxxx"),
    }