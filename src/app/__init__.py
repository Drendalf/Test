from flask import Flask
from flask import render_template
from flask import request

from .config import Config
from .controllers.controller import SafeController
from .controllers.controller import sample_org
from .exceptions import register_errors
from .extensions import db
from .extensions import register_extensions
from .models.model import Itcompanies
from .models.utils import db_init


def create_app(config_class: type[Config]) -> Flask:
    app = Flask(Config.APP_NAME)
    app.config.from_object(config_class)

    register_errors(app)
    register_extensions(app)
    db_init(app)

    @app.route("/", methods=["GET", "POST"])
    def index():
        action = request.values.to_dict()
        if not action:
            return render_template("index.html")
        elif action["action"] == "download":
            SafeController(Itcompanies, db.session).archive_download()

            return render_template("base.html")

    @app.route("/base", methods=["GET", "POST"])
    def base():
        action = request.values.to_dict()

        if not action:
            return render_template("base.html")

        if action["action"] == "start":
            data = sample_org()

            if data:
                for el in data:
                    SafeController(Itcompanies, db.session).create_company(el)
            return render_template("last.html")

    return app
