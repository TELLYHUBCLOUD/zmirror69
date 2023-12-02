from pyrogram import filters
from pyrogram.handlers import MessageHandler

from bot import DATABASE_URL, bot, user_data
from bot.helper.ext_utils.bot_utils import update_user_ldata
from bot.helper.ext_utils.db_handler import DbManager
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage

# Your previous functions...

async def send_sticker_and_message(message, sticker_file_id, text):
    await message.reply_sticker(sticker=sticker_file_id)
    await sendMessage(message, text)

async def authorize(_, message):
    msg = message.text.split()
    if len(msg) > 1:
        id_ = int(msg[1].strip())
    elif reply_to := message.reply_to_message:
        id_ = reply_to.from_user.id
    else:
        id_ = message.chat.id
    if id_ in user_data and user_data[id_].get('is_auth'):
        msg = 'Already Authorized!'
        await send_sticker_and_message(message, 'CAACAgEAAxkBAAEXnGRladqjF5RvYN3ik0edwvnpQwvvZAACTgMAAuGpAAFHKEMLcy3Tm50zBA', msg)
    else:
        update_user_ldata(id_, 'is_auth', True)
        if DATABASE_URL:
            await DbManager().update_user_data(id_)
        msg = 'Authorized Successfully!'
        await send_sticker_and_message(message, 'CAACAgEAAxkBAAEXnGRladqjF5RvYN3ik0edwvnpQwvvZAACTgMAAuGpAAFHKEMLcy3Tm50zBA', msg)

# Modify other functions similarly...

# Replace 'STICKER_FILE_ID_ALREADY_AUTHORIZED' and 'STICKER_FILE_ID_AUTHORIZED_SUCCESSFULLY'
# with the actual file IDs of your stickers.

bot.add_handler(MessageHandler(authorize, filters=filters.command(BotCommands.AuthorizeCommand) & CustomFilters.sudo))
bot.add_handler(MessageHandler(unauthorize, filters=filters.command(BotCommands.UnAuthorizeCommand) & CustomFilters.sudo))
bot.add_handler(MessageHandler(addSudo, filters=filters.command(BotCommands.AddSudoCommand) & CustomFilters.sudo))
bot.add_handler(MessageHandler(removeSudo, filters=filters.command(BotCommands.RmSudoCommand) & CustomFilters.sudo))

# No need for the if __name__ block if this is part of an existing application
