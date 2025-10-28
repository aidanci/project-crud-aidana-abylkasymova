from werkzeug.security import generate_password_hash
from database import get_conn

conn = get_conn()
cur = conn.cursor()

cur.execute("""
INSERT OR IGNORE INTO users (login, password_hash, role)
VALUES (?, ?, ?)
""", ("testuser", generate_password_hash("12345"), "USER"))

conn.commit()
conn.close()
print("✅ Test user created: login='testuser', password='12345'")