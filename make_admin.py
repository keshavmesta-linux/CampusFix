
import getpass
import sqlite3

from app import create_app
from app.db import get_db

app = create_app()

with app.app_context():
    email = input("Existing account email: ").strip().lower()
    password = getpass.getpass("Confirm that account's password: ")

    db = get_db()
    user = db.execute(
        "SELECT id, password_hash FROM users WHERE email = ?",
        (email,),
    ).fetchone()

    if user is None:
        print("Account not found. Register the account first.")
    else:
        from werkzeug.security import check_password_hash

        if not check_password_hash(user["password_hash"], password):
            print("Password did not match. No changes made.")
        else:
            db.execute(
                "UPDATE users SET role = 'admin' WHERE id = ?",
                (user["id"],),
            )
            db.commit()
            print("Admin role assigned successfully.")
