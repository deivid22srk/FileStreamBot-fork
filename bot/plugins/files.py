from hydrogram import filters
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from secrets import token_hex
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.modules.database.json_db import add_file_json, init_json
from bot.modules.telegram import get_file_properties
@TelegramBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.photo
    )
)
@verify_user
async def handle_user_file(_, msg: Message):
    try:
        init_json() # Ensure JSON DB is ready
        sender_id = msg.from_user.id
        secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
        
        # Copy file to channel
        file = await msg.copy(
            chat_id=Telegram.CHANNEL_ID,
            caption=f'||{secret_code}/{sender_id}||'
        )
        file_id = file.id
        
        # Get properties
        file_name, file_size, mime_type = get_file_properties(msg)
        dl_link = f'{Server.BASE_URL}/dl/{file_id}?code={secret_code}'
        stream_link = None
        direct_link = None
        
        if (msg.document and 'video' in msg.document.mime_type) or msg.video:
            stream_link = f'{Server.BASE_URL}/stream/{file_id}?code={secret_code}'
            direct_link = f'{Server.BASE_URL}/dl/{file_id}?code={secret_code}'
            
        # Save to JSON DB
        try:
            add_file_json(file_id, sender_id, secret_code, file_name, file_size, mime_type, dl_link, stream_link, direct_link)
        except Exception as db_err:
            print(f"JSON DB Error (Non-fatal): {db_err}")

        if stream_link:
            await msg.reply(
                text=MediaLinksText % {'dl_link': dl_link, 'stream_link': stream_link, 'direct_link': direct_link},
                quote=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Download', url=dl_link),
                            InlineKeyboardButton('Stream', url=stream_link)
                        ],
                        [
                            InlineKeyboardButton('Direct Link', url=direct_link)
                        ],
                        [
                            InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                        ]
                    ]
                )
            )
        else:
            await msg.reply(
                text=FileLinksText % {'dl_link': dl_link},
                quote=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('Download', url=dl_link),
                            InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                        ]
                    ]
                )
            )
    except Exception as e:
        print(f"Error in handle_user_file: {e}")
        import traceback
        traceback.print_exc()
