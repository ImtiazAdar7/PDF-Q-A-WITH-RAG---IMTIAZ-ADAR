from database import init_db, SessionLocal
from sqlalchemy import text

try:
    db = SessionLocal()
    result = db.execute(text("SELECT version()"))
    print("✅ PostgreSQL connected!")
    print(f"Version: {result.fetchone()[0]}")
    db.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")