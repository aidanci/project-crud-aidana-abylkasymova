from database import get_conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Tworzenie tabeli, jeśli nie istnieje (stare pola)
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

    # Trigger aktualizacji updated_at
    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_planets_updated
        AFTER UPDATE ON planets
        BEGIN
          UPDATE planets SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END;
    """)

    # Dodanie nowych kolumn dla Wymagania B tylko jeśli ich nie ma
    existing_columns = [row["name"] for row in cur.execute("PRAGMA table_info(planets)").fetchall()]

    if "temperature" not in existing_columns:
        cur.execute("ALTER TABLE planets ADD COLUMN temperature TEXT DEFAULT 'unknown';")
    if "terrainType" not in existing_columns:
        cur.execute("ALTER TABLE planets ADD COLUMN terrainType TEXT DEFAULT 'unknown';")

    conn.commit()
    conn.close()
    print("Migracja zakończona, nowe kolumny dodane jeśli brakowało")

if __name__ == "__main__":
    init_db()
