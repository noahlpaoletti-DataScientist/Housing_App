from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_DIR = PROJECT_ROOT / "database"
SCHEMA_DIR = DATABASE_DIR / "schema" / "sqlite"
STORAGE_DIR = DATABASE_DIR / "storage"
DB_PATH = STORAGE_DIR / "housing_app.db"


def apply_schema(conn: sqlite3.Connection) -> None:
    schema_files = sorted(SCHEMA_DIR.glob("*.sql"))
    if not schema_files:
        raise SystemExit(f"No schema files found in {SCHEMA_DIR}")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            filename TEXT PRIMARY KEY,
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    for schema_file in schema_files:
        already_applied = conn.execute(
            "SELECT 1 FROM schema_migrations WHERE filename = ?",
            (schema_file.name,),
        ).fetchone()
        if already_applied:
            continue

        sql_text = schema_file.read_text(encoding="utf-8")
        conn.executescript(sql_text)
        conn.execute(
            "INSERT INTO schema_migrations (filename) VALUES (?)",
            (schema_file.name,),
        )
        conn.commit()
        print(f"Applied schema: {schema_file.name}")


def main() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        apply_schema(conn)

    print(f"SQLite database ready at {DB_PATH}")


if __name__ == "__main__":
    main()
