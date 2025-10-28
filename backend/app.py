from flask import Flask, send_from_directory
from flask_cors import CORS
from pathlib import Path

from .database import init_db
from .planets import bp as planets_bp
from .auth import bp as auth_bp

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

def create_app():
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="/")
    CORS(app)
    init_db()

    app.register_blueprint(planets_bp)
    app.register_blueprint(auth_bp)

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(FRONTEND_DIR, "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=True)
