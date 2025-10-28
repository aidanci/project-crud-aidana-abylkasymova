from flask import Flask, send_from_directory
from flask_cors import CORS
from pathlib import Path

from .database import init_db
from .planets import bp as planets_bp
from .auth import bp as auth_bp


def create_app():
    app = Flask(__name__, static_folder="../frontend", static_url_path="/")
    CORS(app)
    init_db()

    app.register_blueprint(planets_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
