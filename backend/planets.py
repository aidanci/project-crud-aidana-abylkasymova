from flask import Blueprint, jsonify, request
from sqlite3 import IntegrityError
from .database import get_conn
from .validators import validate_planet
from .auth import token_required

bp = Blueprint("planets", __name__, url_prefix="/planets")

@bp.get("/")
@token_required
def list_planets():
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, name, system, climate, population, surface_type AS surfaceType FROM planets ORDER BY id"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@bp.get("/<int:pid>")
@token_required
def get_planet(pid: int):
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, system, climate, population, surface_type AS surfaceType FROM planets WHERE id=?",
        (pid,)
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(dict(row))

@bp.post("/")
@token_required
def create_planet():
    data = request.get_json(silent=True) or {}
    error = validate_planet(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO planets (name, system, climate, population, surface_type) VALUES (?, ?, ?, ?, ?)",
            (data["name"], data["system"], data["climate"], int(data["population"]), data["surfaceType"])
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return jsonify({"message": "Planet created", "id": new_id}), 201
    except IntegrityError:
        return jsonify({"error": "Planet with this name already exists in this system"}), 400

@bp.put("/<int:pid>")
@token_required
def update_planet(pid: int):
    data = request.get_json(silent=True) or {}
    error = validate_planet(data)
    if error:
        return jsonify({"error": error}), 400

    try:
        conn = get_conn()
        cur = conn.cursor()
        exists = conn.execute("SELECT 1 FROM planets WHERE id=?", (pid,)).fetchone()
        if not exists:
            conn.close()
            return jsonify({"error": "Planet not found"}), 404

        cur.execute(
            "UPDATE planets SET name=?, system=?, climate=?, population=?, surface_type=? WHERE id=?",
            (data["name"], data["system"], data["climate"], int(data["population"]), data["surfaceType"], pid)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Planet updated"})
    except IntegrityError:
        return jsonify({"error": "Planet with this name already exists in this system"}), 400

@bp.delete("/<int:pid>")
@token_required
def delete_planet(pid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM planets WHERE id=?", (pid,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    if deleted == 0:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify({"message": "Planet deleted"}), 200