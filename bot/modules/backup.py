import os
import asyncio
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.database.db import DB_PATH, init_db
import sqlite3

async def backup_db():
    if not os.path.exists(DB_PATH):
        return
    
    try:
        await TelegramBot.send_document(
            chat_id=Telegram.CHANNEL_ID,
            document=DB_PATH,
            caption="#BACKUP_DB - Automatic database backup"
        )
    except Exception as e:
        print(f"Backup failed: {e}")

async def restore_db():
    init_db()
    # Se o banco de dados já existir e não estiver vazio, não restaurar para evitar sobrescrever dados novos
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 1024: # Mais de 1KB
        print("Local database already exists and is not empty. Skipping restore.")
        return True

    try:
        print("Searching for backup in Telegram...")
        async for message in TelegramBot.get_chat_history(Telegram.CHANNEL_ID, limit=100):
            if message.caption and "#BACKUP_DB" in message.caption:
                if message.document:
                    print(f"Found backup message ID: {message.id}. Downloading...")
                    await TelegramBot.download_media(message, file_name=DB_PATH)
                    print("Database restored from Telegram successfully.")
                    return True
        print("No backup found in the last 100 messages.")
    except Exception as e:
        print(f"Restore failed: {e}")
    return False

async def start_backup_loop():
    while True:
        await asyncio.sleep(3600) # Backup every hour
        await backup_db()
