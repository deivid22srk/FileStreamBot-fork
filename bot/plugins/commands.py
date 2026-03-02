from hydrogram import filters
from hydrogram.types import Message
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user
from bot.modules.backup import backup_db, restore_db
@TelegramBot.on_message(filters.command(['start', 'help']) & filters.private)
@verify_user
async def start_command(_, msg: Message):
    await msg.reply(
        text = WelcomeText % {'first_name': msg.from_user.first_name},
        quote = True
    )

@TelegramBot.on_message(filters.command('privacy') & filters.private)
@verify_user
async def privacy_command(_, msg: Message):
    await msg.reply(text=PrivacyText, quote=True, disable_web_page_preview=True)

@TelegramBot.on_message(filters.command('log') & filters.chat(Telegram.OWNER_ID))
async def log_command(_, msg: Message):
    await msg.reply_document('event-log.txt', quote=True)

@TelegramBot.on_message(filters.command('backup') & filters.chat(Telegram.OWNER_ID))
async def manual_backup(_, msg: Message):
    await backup_db()
    await msg.reply("Backup manual concluído e enviado para o canal.")

@TelegramBot.on_message(filters.command('restore') & filters.chat(Telegram.OWNER_ID))
async def manual_restore(_, msg: Message):
    success = await restore_db()
    if success:
        await msg.reply("Banco de dados restaurado com sucesso do canal.")
    else:
        await msg.reply("Falha ao restaurar o banco de dados ou backup não encontrado.")
