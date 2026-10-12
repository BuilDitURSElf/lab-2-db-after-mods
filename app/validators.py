"""[R8] Validation rules with the exact messages from the lab.

The server runs these again even though JavaScript already checked in the browser,
because anybody can send a request without using our page.
Each function returns a dict {field_name: message}; an empty dict means "all good".
"""
from datetime import date

MAX_NAME = 100        # users.name is VARCHAR(100)
MAX_EMAIL = 255       # users.email is VARCHAR(255)
MAX_TITLE = 200       # todos.title is VARCHAR(200)
MAX_PASSWORD_BYTES = 72  # bcrypt only reads the first 72 bytes


def validate_register(name, email, password, confirm_password):
    errors = {}
    if not name.strip():
        errors["name"] = "Name is required"
    elif len(name) > MAX_NAME:
        errors["name"] = f"Name is too long ({MAX_NAME} characters at most)"

    if not email.strip():
        errors["email"] = "Email is required"
    elif len(email) > MAX_EMAIL:
        errors["email"] = f"Email is too long ({MAX_EMAIL} characters at most)"

    if not password:
        errors["password"] = "Password is required"
    elif len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        errors["password"] = f"Password is too long ({MAX_PASSWORD_BYTES} characters at most)"

    if not confirm_password:
        errors["confirm_password"] = "Confirm password is required"
    elif password != confirm_password:
        errors["confirm_password"] = "Passwords do not match"
    return errors


def validate_login(email, password):
    errors = {}
    if not email.strip():
        errors["email"] = "Email is required"
    if not password:
        errors["password"] = "Password is required"
    return errors


def validate_title(title):
    """Used for both adding and editing a to-do. Returns a message or None."""
    if not title.strip():  # empty or only spaces
        return "Title is required"
    if len(title.strip()) > MAX_TITLE:
        return f"Title is too long ({MAX_TITLE} characters at most)"
    return None


def parse_due_date(text):
    """[Bonus: due dates] Returns (date or None, error message or None). An empty field is allowed."""
    text = text.strip()
    if not text:
        return None, None
    try:
        return date.fromisoformat(text), None  # the browser sends YYYY-MM-DD
    except ValueError:
        return None, "Due date is not a valid date"
