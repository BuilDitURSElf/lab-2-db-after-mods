"""Settings read from the .env file.

[R9] Secrets (database password, session secret) are never written in the code.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")  # signs the session cookie
    SESSION_COOKIE_SAMESITE = "Lax"  # browser will not send the cookie on cross-site POSTs
    # [Bonus: deploy] on an https website set COOKIE_SECURE=1 so the cookie is never sent over http
    SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "0") == "1"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "registration")
