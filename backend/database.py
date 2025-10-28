import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "planets.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS planets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            system TEXT NOT NULL,
            climate TEXT NOT NULL,
            population INTEGER NOT NULL CHECK (population >= 0),
            surface_type TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, system)
        );
    """)

    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_planets_updated
        AFTER UPDATE ON planets
        BEGIN
            UPDATE planets SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'USER',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
