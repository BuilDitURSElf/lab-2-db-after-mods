"""All SQL about the users table. Nothing else in the project writes SQL for users."""
import pymysql

from app.db import get_db

MYSQL_DUPLICATE_ENTRY = 1062  # error code when a UNIQUE column gets a repeated value


class DuplicateEmailError(Exception):
    """Raised when the e-mail is already registered."""


def create_user(email, name, password_hash):
    """Sign up. [R9] values are passed separately (%s), never glued into the SQL."""
    try:
        with get_db().cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                (email, name, password_hash),
            )
            return cur.lastrowid
    except pymysql.err.IntegrityError as error:
        if error.args[0] == MYSQL_DUPLICATE_ENTRY:  # [R1] UNIQUE (email) was violated
            raise DuplicateEmailError() from error
        raise


def find_by_email(email):
    """Log in: find the user by e-mail (the password is compared in Python, not in SQL)."""
    with get_db().cursor() as cur:
        cur.execute(
            "SELECT user_id, name, password_hash FROM users WHERE email = %s",
            (email,),
        )
        return cur.fetchone()  # a dict, or None when the e-mail is unknown
