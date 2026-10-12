"""To-do pages: list, add, edit title, mark done, delete. All of them are private."""
from flask import Blueprint, redirect, render_template, request, url_for

from app.repositories import todos as todos_repo
from app.security import current_user_id, login_required
from app.validators import validate_title

bp = Blueprint("todos", __name__)


def render_list(add_value="", add_error="", edit_id=None, edit_value="", edit_error=""):
    """Show the page. Used for the normal view AND to show validation errors again."""
    items = todos_repo.list_for_user(current_user_id())  # [R3] only this user's to-dos
    return render_template(
        "todos.html",
        todos=items,
        add_value=add_value,
        add_error=add_error,
        edit_id=edit_id,
        edit_value=edit_value,
        edit_error=edit_error,
    )


@bp.route("/")
@login_required  # [R3] not logged in -> redirected to the login page
def index():
    return render_list()


@bp.post("/todos/add")
@login_required
def add():
    title = request.form.get("title", "").strip()
    error = validate_title(title)  # [R8]
    if error:
        return render_list(add_value=title, add_error=error), 400  # database not touched
    todos_repo.add(current_user_id(), title)  # [R4] user_id from the session
    return redirect(url_for("todos.index"))


@bp.post("/todos/<int:todo_id>/edit")
@login_required
def edit(todo_id):
    title = request.form.get("title", "").strip()
    error = validate_title(title)  # [R8]
    if error:
        return render_list(edit_id=todo_id, edit_value=title, edit_error=error), 400
    todos_repo.update_title(todo_id, current_user_id(), title)  # [R5]
    return redirect(url_for("todos.index"))


@bp.post("/todos/<int:todo_id>/toggle")
@login_required
def toggle(todo_id):
    is_done = 1 if request.form.get("is_done") == "1" else 0  # only 0 or 1 is possible
    todos_repo.set_done(todo_id, current_user_id(), is_done)  # [R6]
    return redirect(url_for("todos.index"))


@bp.post("/todos/<int:todo_id>/delete")
@login_required
def delete(todo_id):
    todos_repo.delete(todo_id, current_user_id())  # [R7] (the browser asked "are you sure?")
    return redirect(url_for("todos.index"))
