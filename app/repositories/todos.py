"""All SQL about the todos table: exactly the five queries given in the lab.

[R9] Every statement uses %s placeholders.
[R3][R5][R6][R7] UPDATE and DELETE end with "AND user_id = %s", so a user can
never change somebody else's to-do (zero rows are changed instead).
"""
from app.db import get_db


def list_for_user(user_id):
    """[R3] Only this user's to-dos, newest first."""
    with get_db().cursor() as cur:
        cur.execute(
            "SELECT todo_id, title, is_done, created_at FROM todos "
            "WHERE user_id = %s ORDER BY todo_id DESC",
            (user_id,),
        )
        return cur.fetchall()


def add(user_id, title):
    """[R4] Add a to-do."""
    with get_db().cursor() as cur:
        cur.execute(
            "INSERT INTO todos (user_id, title) VALUES (%s, %s)",
            (user_id, title),
        )


def update_title(todo_id, user_id, title):
    """[R5] Edit the title."""
    with get_db().cursor() as cur:
        cur.execute(
            "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
            (title, todo_id, user_id),
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
