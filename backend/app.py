from flask import Flask, send_from_directory
from flask_cors import CORS
from pathlib import Path

from .database import init_db
from .planets import bp as planets_bp

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

def create_app():
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="/")
    CORS(app)

    init_db()  # создаем таблицу и новые колонки при старте

    app.register_blueprint(planets_bp)

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    return app

# ⚠️ создаём объект app глобально
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
