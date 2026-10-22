
import re
import sqlite3

from flask import (
    Blueprint, flash, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import get_db

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        error = None

        if len(name) < 2 or len(name) > 80:
            error = "Name must be between 2 and 80 characters."
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            error = "Enter a valid email address."
        elif len(email) > 254:
            error = "Email address is too long."
        elif len(password) < 10 or len(password) > 128:
            error = "Password must be 10–128 characters."

        db = get_db()

        if error is None:
            try:
                db.execute(
                    """
                    INSERT INTO users (name, email, password_hash)
                    VALUES (?, ?, ?)
                    """,
                    (name, email, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = "That email is already registered."

        if error:
            flash(error, "error")
        else:
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_db().execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        if user is None or not check_password_hash(
            user["password_hash"], password
        ):
            flash("Invalid email or password.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["user_role"] = user["role"]
            session["user_name"] = user["name"]

            flash("Welcome back!", "success")
            return redirect(url_for("index"))

    return render_template("login.html")


@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))
