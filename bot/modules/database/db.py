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
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_file(file_id, sender_id, secret_code, file_name, file_size):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO files (file_id, sender_id, secret_code, file_name, file_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_id, sender_id, secret_code, file_name, file_size))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_all_files():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files')
    rows = cursor.fetchall()
    conn.close()
    return rows
