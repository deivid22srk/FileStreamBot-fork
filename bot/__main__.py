from bot import TelegramBot
from bot.server import server
from bot.modules.database.json_db import init_json
from bot.modules.backup import restore_db, start_backup_loop
import asyncio

async def main():
    init_json()
    await TelegramBot.start()
    await restore_db()
    TelegramBot.loop.create_task(server.serve())
    TelegramBot.loop.create_task(start_backup_loop())
    print("Bot started!")
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        TelegramBot.loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the web server if it's running
        if server.started:
            TelegramBot.loop.run_until_complete(server.shutdown())
        TelegramBot.loop.run_until_complete(TelegramBot.stop())
