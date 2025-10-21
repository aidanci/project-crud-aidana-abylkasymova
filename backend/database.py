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

    # Создание таблицы planets
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

    # Триггер обновления updated_at
    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_planets_updated
        AFTER UPDATE ON planets
        BEGIN
            UPDATE planets SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
    """)

    # Добавление новых колонок, если их нет
    existing_columns = [row["name"] for row in cur.execute("PRAGMA table_info(planets)").fetchall()]
    if "temperature" not in existing_columns:
        cur.execute("ALTER TABLE planets ADD COLUMN temperature TEXT DEFAULT 'unknown';")
    if "terrainType" not in existing_columns:
        cur.execute("ALTER TABLE planets ADD COLUMN terrainType TEXT DEFAULT 'unknown';")

    conn.commit()
    conn.close()
    print("Migration finished: new columns added if missing")
