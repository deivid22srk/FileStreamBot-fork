import os
import asyncio
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.database.json_db import JSON_PATH, init_json
import sqlite3

async def backup_db():
    if not os.path.exists(JSON_PATH):
        return
    
    try:
        await TelegramBot.send_document(
            chat_id=Telegram.CHANNEL_ID,
            document=JSON_PATH,
            caption="#BACKUP_JSON - Automatic JSON data backup"
        )
    except Exception as e:
        print(f"Backup failed: {e}")

async def restore_db():
    init_json()
    # Se o arquivo JSON já existir e não estiver vazio, não restaurar para evitar sobrescrever dados novos
    if os.path.exists(JSON_PATH) and os.path.getsize(JSON_PATH) > 10: # Mais de 10 bytes (um JSON vazio [] tem 2 bytes)
        print("Local JSON data already exists and is not empty. Skipping restore.")
        return True

    try:
        print("Searching for JSON backup in Telegram...")
        async for message in TelegramBot.get_chat_history(Telegram.CHANNEL_ID, limit=100):
            if message.caption and "#BACKUP_JSON" in message.caption:
                if message.document:
                    print(f"Found backup message ID: {message.id}. Downloading...")
                    await TelegramBot.download_media(message, file_name=JSON_PATH)
                    print("JSON data restored from Telegram successfully.")
                    return True
        print("No JSON backup found in the last 100 messages.")
    except Exception as e:
        print(f"Restore failed: {e}")
    return False

async def start_backup_loop():
    while True:
        await asyncio.sleep(3600) # Backup every hour
        await backup_db()
