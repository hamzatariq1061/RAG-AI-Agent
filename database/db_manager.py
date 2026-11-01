
import sqlite3
from pathlib import Path

DB_PATH = Path("storage/documents.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_hash TEXT UNIQUE NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def document_exists(file_hash):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT id FROM documents WHERE file_hash = ?",
            (file_hash,)
        ).fetchone()

    return result is not None


def save_document(filename, file_hash):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO documents (filename, file_hash) VALUES (?, ?)",
            (filename, file_hash)
        )


def get_all_documents():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, filename, uploaded_at FROM documents ORDER BY id DESC"
        ).fetchall()


initialize_database()
