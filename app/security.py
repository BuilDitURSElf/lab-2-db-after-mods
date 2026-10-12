"""Passwords and sessions."""
from functools import wraps

import bcrypt
from flask import redirect, session, url_for


def hash_password(password):
    """[R9] bcrypt hash: salted (same password -> different hash) and slow on purpose."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password, password_hash):
    """[R2] Ask bcrypt to compare the typed password with the stored hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def login_user(user_id, name):
    """[R1][R2] Remember who is logged in. The cookie only holds a signed session id."""
    session.clear()
    session["user_id"] = user_id
    session["name"] = name


def logout_user():
    """[R2] Logout destroys the session."""
    session.clear()


def current_user_id():
    """[R9] The only place the user_id comes from is the session, never from a form."""
    return session.get("user_id")


def login_required(view):
    """[R3] Private pages: a visitor who is not logged in is sent to the login page."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user_id() is None:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped
