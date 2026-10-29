"""
Quick Mart - Database Initialization Utility
Creates or resets the SQLite database using database/quickmart_schema_and_seed.sql.
"""

import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "quickmart.db"
SQL_PATH = BASE_DIR / "database" / "quickmart_schema_and_seed.sql"

def init_database():
    print(f"Connecting to database: {DB_PATH}")
    if not SQL_PATH.exists():
        print(f"Error: SQL dump script not found at {SQL_PATH}")
        return False

    with open(SQL_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(sql_content)
        conn.commit()
        print("Database schema and seed records initialized successfully!")

        cur = conn.cursor()
        for tbl in ["users", "suppliers", "products", "bills", "bill_items"]:
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            count = cur.fetchone()[0]
            print(f" - {tbl}: {count} records loaded.")

        cur.execute("PRAGMA foreign_key_check;")
        fk_violations = cur.fetchall()
        if fk_violations:
            print(f"Warning: Foreign key violations detected: {fk_violations}")
        else:
            print(" - Foreign key integrity: 100% OK")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
