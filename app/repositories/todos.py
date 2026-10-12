"""All SQL about the todos table: the five queries given in the lab.
(Bonus: INSERT and UPDATE also carry the optional due_date column.)

[R9] Every statement uses %s placeholders.
[R3][R5][R6][R7] UPDATE and DELETE end with "AND user_id = %s", so a user can
never change somebody else's to-do (zero rows are changed instead).
"""
from app.db import get_db


def list_for_user(user_id):
    """[R3] Only this user's to-dos, newest first."""
    with get_db().cursor() as cur:
        cur.execute(
            "SELECT todo_id, title, is_done, due_date, created_at FROM todos "
            "WHERE user_id = %s ORDER BY todo_id DESC",
            (user_id,),
        )
        return cur.fetchall()


def add(user_id, title, due_date=None):
    """[R4] Add a to-do (due_date is the optional bonus field)."""
    with get_db().cursor() as cur:
        cur.execute(
            "INSERT INTO todos (user_id, title, due_date) VALUES (%s, %s, %s)",
            (user_id, title, due_date),
        )


def update_title(todo_id, user_id, title, due_date=None):
    """[R5] Edit the title (and the optional due date)."""
    with get_db().cursor() as cur:
        cur.execute(
            "UPDATE todos SET title = %s, due_date = %s WHERE todo_id = %s AND user_id = %s",
            (title, due_date, todo_id, user_id),
        )


def set_done(todo_id, user_id, is_done):
    """[R6] Mark done (1) or not done (0)."""
    with get_db().cursor() as cur:
        cur.execute(
            "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
            (is_done, todo_id, user_id),
        )


def delete(todo_id, user_id):
    """[R7] Delete."""
    with get_db().cursor() as cur:
        cur.execute(
            "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
            (todo_id, user_id),
        )
