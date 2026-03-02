from bot import TelegramBot
from bot.server import server
from bot.modules.database.db import init_db
from bot.modules.backup import restore_db, start_backup_loop
import asyncio

async def main():
    init_db()
    await restore_db()
    TelegramBot.loop.create_task(server.serve())
    TelegramBot.loop.create_task(start_backup_loop())
    await TelegramBot.start()
    print("Bot started!")
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        TelegramBot.loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        TelegramBot.loop.run_until_complete(TelegramBot.stop())
