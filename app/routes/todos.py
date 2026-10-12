"""To-do pages: list, add, edit title, mark done, delete. All of them are private."""
from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from app.repositories import todos as todos_repo
from app.security import current_user_id, login_required
from app.validators import parse_due_date, validate_title

bp = Blueprint("todos", __name__)

FILTERS = ("all", "open", "done")  # [Bonus: filters] the three tabs above the list


def get_filter():
    """[Bonus: filters] The selected tab comes from the address (?filter=open). Unknown = all."""
    status = request.args.get("filter", "all")
    return status if status in FILTERS else "all"


def get_search():
    """[Bonus: search] The search text comes from the address (?q=milk)."""
    return request.args.get("q", "").strip()[:200]


def list_args():
    """The selected tab + search text, as address arguments (empty ones are left out)."""
    status = get_filter()
    return {"filter": None if status == "all" else status, "q": get_search() or None}


def back_to_list():
    """Redirect after a POST, keeping the selected tab and the search text."""
    return redirect(url_for("todos.index", **list_args()))


def render_list(add_value="", add_error="", edit_id=None, edit_value="", edit_error="",
                add_due="", edit_due=""):
    """Show the page. Used for the normal view AND to show validation errors again."""
    all_items = todos_repo.list_for_user(current_user_id())  # [R3] only this user's to-dos

    # [Bonus: search + filters] Both are done in Python on the list we already have,
    # so no extra SQL query is needed.
    search = get_search()
    items = [t for t in all_items if search.lower() in t["title"].lower()] if search else all_items
    status = get_filter()
    open_items = [t for t in items if not t["is_done"]]
    done_items = [t for t in items if t["is_done"]]
    visible = {"all": items, "open": open_items, "done": done_items}[status]

    return render_template(
        "todos.html",
        todos=visible,
        status=status,
        search=search,
        args=list_args(),
        all_count=len(all_items),                                    # whole list (header)
        all_open_count=sum(1 for t in all_items if not t["is_done"]),
        total_count=len(items),                                      # matches of the search (tabs)
        open_count=len(open_items),
        done_count=len(done_items),
        today=date.today(),  # [Bonus: due dates] used to mark overdue to-dos
        add_value=add_value,
        add_error=add_error,
        add_due=add_due,
        edit_id=edit_id,
        edit_value=edit_value,
        edit_error=edit_error,
        edit_due=edit_due,
    )


@bp.route("/")
@login_required  # [R3] not logged in -> redirected to the login page
def index():
    return render_list()


@bp.post("/todos/add")
@login_required
def add():
    title = request.form.get("title", "").strip()
    due_raw = request.form.get("due_date", "")
    error = validate_title(title)  # [R8]
    due_date, due_error = parse_due_date(due_raw)  # [Bonus: due dates]
    if error or due_error:
        return render_list(add_value=title, add_error=error or due_error, add_due=due_raw), 400
    todos_repo.add(current_user_id(), title, due_date)  # [R4] user_id from the session
    return back_to_list()


@bp.post("/todos/<int:todo_id>/edit")
@login_required
def edit(todo_id):
    title = request.form.get("title", "").strip()
    due_raw = request.form.get("due_date", "")
    error = validate_title(title)  # [R8]
    due_date, due_error = parse_due_date(due_raw)  # [Bonus: due dates]
    if error or due_error:
        return render_list(edit_id=todo_id, edit_value=title, edit_error=error or due_error,
                           edit_due=due_raw), 400
    todos_repo.update_title(todo_id, current_user_id(), title, due_date)  # [R5]
    return back_to_list()


@bp.post("/todos/<int:todo_id>/toggle")
@login_required
def toggle(todo_id):
    is_done = 1 if request.form.get("is_done") == "1" else 0  # only 0 or 1 is possible
    todos_repo.set_done(todo_id, current_user_id(), is_done)  # [R6]
    return back_to_list()


@bp.post("/todos/<int:todo_id>/delete")
@login_required
def delete(todo_id):
    todos_repo.delete(todo_id, current_user_id())  # [R7] (the browser asked "are you sure?")
    return back_to_list()
