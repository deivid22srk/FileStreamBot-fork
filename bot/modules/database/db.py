import sqlite3
import os
from bot.config import Telegram

DB_PATH = "filestream.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER UNIQUE,
            sender_id INTEGER,
            secret_code TEXT,
            file_name TEXT,
            file_size INTEGER,
            mime_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_file(file_id, sender_id, secret_code, file_name, file_size, mime_type):
    conn = sqlite3.connect(DB_PATH, isolation_level=None) # Auto-commit mode
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO files (file_id, sender_id, secret_code, file_name, file_size, mime_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (file_id, sender_id, secret_code, file_name, file_size, mime_type))
        print(f"Database: File {file_name} (ID: {file_id}) saved successfully.")
    except Exception as e:
        print(f"Database Error: Failed to save file {file_name}. Error: {e}")
    finally:
        conn.close()

def get_all_files():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files')
    rows = cursor.fetchall()
    conn.close()
    return rows
