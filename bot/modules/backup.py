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
    try:
        async for message in TelegramBot.get_chat_history(Telegram.CHANNEL_ID, limit=50):
            if message.caption and "#BACKUP_DB" in message.caption:
                if message.document:
                    await TelegramBot.download_media(message, file_name=DB_PATH)
                    print("Database restored from Telegram.")
                    return True
    except Exception as e:
        print(f"Restore failed: {e}")
    return False

async def start_backup_loop():
    while True:
        await asyncio.sleep(3600) # Backup every hour
        await backup_db()
