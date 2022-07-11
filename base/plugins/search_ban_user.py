from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters
from decouple import config

from base.sql.db_methods import get_user, update_user

# Ban user from bot
@Client.on_message(filters.private & filters.user(config("OWNER")) & filters.reply & filters.regex("/ban_id"))
def ban_id(client: Client, message: Message):
    target_username = message.reply_to_message.text
    if "@" in target_username:
        target_username = target_username[1:]

    target_user = get_user(username=target_username)
    if not target_username:
        message.reply(
            "This user does not exist in bot!"
        )
        return 0

    target_user.is_banned = True
    update_user(target_user)
    message.reply(
        "The user has been banned from bot!"
    )