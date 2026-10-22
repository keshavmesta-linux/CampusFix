
import os
from pathlib import Path

from flask import Flask
from app.admin import admin as admin_blueprint
from app.db import init_app as init_database
from app.reports import reports as reports_blueprint

def create_app():
    
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.environ.get("CAMPUSFIX_SECRET_KEY")

    if not app.config["SECRET_KEY"]:
        raise RuntimeError(
            "Set CAMPUSFIX_SECRET_KEY before starting CampusFix."
        )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app.config["DATABASE"] = str(
        Path(app.instance_path) / "campusfix.db"
    )

    init_database(app)
    from flask import render_template

    from app.auth import auth
    app.register_blueprint(auth)
    app.register_blueprint(reports_blueprint)
    app.register_blueprint(admin_blueprint)
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

