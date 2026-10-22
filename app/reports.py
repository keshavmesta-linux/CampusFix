
from flask import (
    Blueprint, flash, jsonify, redirect, render_template,
    request, session, url_for
)
from flask import (
    Blueprint, flash, redirect, render_template,
    request, session, url_for
)

from app.db import get_db

reports = Blueprint("reports", __name__)

CATEGORIES = [
    "Water Supply",
    "Electricity",
    "Cleanliness",
    "Classroom",
    "Washroom",
    "Furniture",
    "Internet",
    "Other",
]


def login_required(view):
    from functools import wraps

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


@reports.route("/report/new", methods=["GET", "POST"])
@login_required
def create_report():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        location = request.form.get("location", "").strip()

        error = None

        if not 5 <= len(title) <= 100:
            error = "Title must be between 5 and 100 characters."
        elif not 10 <= len(description) <= 2000:
            error = "Description must be between 10 and 2000 characters."
        elif category not in CATEGORIES:
            error = "Choose a valid category."
        elif not 2 <= len(location) <= 150:
            error = "Location must be between 2 and 150 characters."

        if error:
            flash(error, "error")
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO reports
                    (user_id, title, description, category, location)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session["user_id"],
                    title,
                    description,
                    category,
                    location,
                ),
            )
            db.commit()

            flash("Your issue report was submitted!", "success")
            return redirect(url_for("reports.my_reports"))

    return render_template("report_new.html", categories=CATEGORIES)


@reports.route("/my-reports")
@login_required
def my_reports():
    db = get_db()
    user_reports = db.execute(
        """
        SELECT id, title, category, location, status, created_at
        FROM reports
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (session["user_id"],),
    ).fetchall()

    return render_template("my_reports.html", reports=user_reports)
@reports.route("/api/my-reports")
@login_required
def my_reports_api():
    db = get_db()

    rows = db.execute(
        """
        SELECT id, status, updated_at
        FROM reports
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (session["user_id"],),
    ).fetchall()

    return jsonify([
        {
            "id": row["id"],
            "status": row["status"],
            "updated_at": row["updated_at"],
        }
        for row in rows
    ])

@reports.route("/notifications")
@login_required
def notifications():
    db = get_db()

    user_notifications = db.execute(
        """
        SELECT id, report_id, message, is_read, created_at
        FROM notifications
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (session["user_id"],),
    ).fetchall()

    return render_template(
        "notifications.html",
        notifications=user_notifications,
    )


@reports.route("/notifications/<int:notification_id>/read", methods=["POST"])
@login_required
def mark_notification_read(notification_id):
    db = get_db()

    db.execute(
        """
        UPDATE notifications
        SET is_read = 1
        WHERE id = ? AND user_id = ?
        """,
        (notification_id, session["user_id"]),
    )
    db.commit()

    return redirect(url_for("reports.notifications"))

@reports.route("/api/notifications/unread-count")
@login_required
def unread_notification_count():
    db = get_db()

    row = db.execute(
        """
        SELECT COUNT(*) AS total
        FROM notifications
        WHERE user_id = ? AND is_read = 0
        """,
        (session["user_id"],),
    ).fetchone()

    return jsonify({"count": row["total"]})
