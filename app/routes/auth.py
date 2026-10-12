"""Auth pages: register, login, logout."""
from flask import Blueprint, redirect, render_template, request, url_for

from app.repositories import users as users_repo
from app.security import (
    current_user_id,
    hash_password,
    login_user,
    logout_user,
    verify_password,
)
from app.validators import validate_login, validate_register

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user_id() is not None:
        return redirect(url_for("todos.index"))
    if request.method == "GET":
        return render_template("register.html", errors={}, form={})

    # [R1] read the four fields of the form
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    # [R8] server-side check: on error show the same page and do NOT touch the database
    errors = validate_register(name, email, password, confirm_password)
    if errors:
        return render_template("register.html", errors=errors, form={"name": name, "email": email}), 400

    try:
        user_id = users_repo.create_user(email, name, hash_password(password))  # [R9]
    except users_repo.DuplicateEmailError:
        errors = {"email": "Email Already Exists"}  # [R1]
        return render_template("register.html", errors=errors, form={"name": name, "email": email}), 409

    login_user(user_id, name)  # [R1] registered users are logged in straight away
    return redirect(url_for("todos.index"))  # redirect after POST: refresh does not resend the form


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user_id() is not None:
        return redirect(url_for("todos.index"))
    if request.method == "GET":
        return render_template("login.html", errors={}, form={})

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # [R8] server-side check
    errors = validate_login(email, password)
    if errors:
        return render_template("login.html", errors=errors, form={"email": email}), 400

    user = users_repo.find_by_email(email)
    # [R2] unknown e-mail and wrong password give the SAME message
    if user is None or not verify_password(password, user["password_hash"]):
        errors = {"form": "Invalid email or password"}
        return render_template("login.html", errors=errors, form={"email": email}), 401

    login_user(user["user_id"], user["name"])
    return redirect(url_for("todos.index"))


@bp.post("/logout")
def logout():
    logout_user()  # [R2]
    return redirect(url_for("auth.login"))
