"""Automated tests (bonus). They replace the two repositories with in-memory fakes,
so they run without MySQL and check the application logic: routes, validation,
sessions, privacy and password hashing.
"""
import pytest

from app import create_app
from app.repositories import todos as todos_repo
from app.repositories import users as users_repo


@pytest.fixture
def client(monkeypatch):
    users = {}  # email -> row
    todos = []  # list of rows

    def create_user(email, name, password_hash):
        if email in users:
            raise users_repo.DuplicateEmailError()
        users[email] = {"user_id": len(users) + 1, "name": name, "password_hash": password_hash}
        return users[email]["user_id"]

    def find_by_email(email):
        return users.get(email)

    def list_for_user(user_id):
        return sorted((t for t in todos if t["user_id"] == user_id), key=lambda t: -t["todo_id"])

    def add(user_id, title):
        todos.append({"todo_id": len(todos) + 1, "user_id": user_id, "title": title, "is_done": 0})

    def update_title(todo_id, user_id, title):
        for t in todos:
            if t["todo_id"] == todo_id and t["user_id"] == user_id:
                t["title"] = title

    def set_done(todo_id, user_id, is_done):
        for t in todos:
            if t["todo_id"] == todo_id and t["user_id"] == user_id:
                t["is_done"] = is_done

    def delete(todo_id, user_id):
        todos[:] = [t for t in todos if not (t["todo_id"] == todo_id and t["user_id"] == user_id)]

    monkeypatch.setattr(users_repo, "create_user", create_user)
    monkeypatch.setattr(users_repo, "find_by_email", find_by_email)
    monkeypatch.setattr(todos_repo, "list_for_user", list_for_user)
    monkeypatch.setattr(todos_repo, "add", add)
    monkeypatch.setattr(todos_repo, "update_title", update_title)
    monkeypatch.setattr(todos_repo, "set_done", set_done)
    monkeypatch.setattr(todos_repo, "delete", delete)

    app = create_app()
    app.config["TESTING"] = True
    test_client = app.test_client()
    test_client.fake_users = users
    test_client.fake_todos = todos
    return test_client


def register(client, name="Sara", email="sara@mail.com", password="secret1", confirm=None):
    return client.post(
        "/register",
        data={"name": name, "email": email, "password": password,
              "confirm_password": password if confirm is None else confirm},
    )


def new_browser(client):
    """A second browser = a second client with its own cookies, sharing the same fake data."""
    other = client.application.test_client()
    other.fake_users = client.fake_users
    other.fake_todos = client.fake_todos
    return other


def test_list_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_register_empty_form_shows_one_message_per_field(client):
    response = client.post("/register", data={})
    page = response.get_data(as_text=True)
    for message in ["Name is required", "Email is required", "Password is required",
                    "Confirm password is required"]:
        assert message in page
    assert client.fake_users == {}  # the database was not touched


def test_register_passwords_do_not_match(client):
    page = register(client, confirm="different").get_data(as_text=True)
    assert "Passwords do not match" in page
    assert client.fake_users == {}


def test_register_logs_the_user_in(client):
    response = register(client)
    assert response.status_code == 302
    assert "Hi, Sara" in client.get("/").get_data(as_text=True)


def test_duplicate_email(client):
    register(client)
    other = new_browser(client)
    assert "Email Already Exists" in register(other).get_data(as_text=True)


def test_password_is_stored_as_bcrypt_hash(client):
    register(client)
    stored = client.fake_users["sara@mail.com"]["password_hash"]
    assert stored.startswith("$2b$12$")
    assert "secret1" not in stored


def test_login_same_message_for_wrong_password_and_unknown_email(client):
    register(client)
    other = new_browser(client)
    wrong_password = other.post("/login", data={"email": "sara@mail.com", "password": "nope"})
    unknown_email = other.post("/login", data={"email": "who@mail.com", "password": "secret1"})
    assert "Invalid email or password" in wrong_password.get_data(as_text=True)
    assert "Invalid email or password" in unknown_email.get_data(as_text=True)


def test_login_sql_injection_text_does_not_log_in(client):
    register(client)
    other = new_browser(client)
    response = other.post("/login", data={"email": "' OR '1'='1' --", "password": "x"})
    assert "Invalid email or password" in response.get_data(as_text=True)
    assert other.get("/").status_code == 302


def test_login_empty_form(client):
    page = client.post("/login", data={}).get_data(as_text=True)
    assert "Email is required" in page and "Password is required" in page


def test_logout_ends_the_session(client):
    register(client)
    client.post("/logout")
    assert client.get("/").status_code == 302


def test_add_edit_done_delete(client):
    register(client)
    client.post("/todos/add", data={"title": "Buy oat milk"})
    assert "Buy oat milk" in client.get("/").get_data(as_text=True)

    client.post("/todos/1/edit", data={"title": "Buy almond milk"})
    assert client.fake_todos[0]["title"] == "Buy almond milk"

    client.post("/todos/1/toggle", data={"is_done": "1"})
    assert client.fake_todos[0]["is_done"] == 1
    assert 'class="todo done"' in client.get("/").get_data(as_text=True)

    client.post("/todos/1/delete")
    assert client.fake_todos == []
    assert "Nothing to do yet" in client.get("/").get_data(as_text=True)


def test_title_validation(client):
    register(client)
    assert "Title is required" in client.post("/todos/add", data={"title": "   "}).get_data(as_text=True)
    too_long = client.post("/todos/add", data={"title": "x" * 201}).get_data(as_text=True)
    assert "Title is too long (200 characters at most)" in too_long
    assert client.fake_todos == []


def test_users_only_see_and_change_their_own_todos(client):
    register(client)
    client.post("/todos/add", data={"title": "Sara's secret"})

    omar = new_browser(client)
    register(omar, name="Omar", email="omar@mail.com")
    assert "Sara's secret" not in omar.get("/").get_data(as_text=True)

    # Omar sends Sara's to-do number: nothing changes
    omar.post("/todos/1/edit", data={"title": "hacked"})
    omar.post("/todos/1/toggle", data={"is_done": "1"})
    omar.post("/todos/1/delete")
    assert client.fake_todos[0]["title"] == "Sara's secret"
    assert client.fake_todos[0]["is_done"] == 0


def test_unknown_page_shows_friendly_error(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert "Back to my list" in response.get_data(as_text=True)
