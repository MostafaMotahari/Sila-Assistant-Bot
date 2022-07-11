from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters
from decouple import config

from base.sql.session import get_db
from base.sql.models import UserModel

# Ban user from
@Client.on_message(filters.private & filters.user(config("OWNER")) & filters.reply & filters.regex("/ban_id"))
def ban_id(client: Client, message: Message):
    target_username = message.reply_to_message.text

    if "@" in target_username:
        target_username = target_username[1:]

    db_session = get_db().__next__()
    target_user = db_session.query(UserModel).filter(UserModel.username == target_username).first()

    if not target_user:
        message.reply(
            "This user does not exist in bot!"
        )
        return 0

    target_user.is_banned = True
    db_session.commit()

    message.reply(
        "The user has been banned from bot!"
    )


# UnBan user from
@Client.on_message(filters.private & filters.user(config("OWNER")) & filters.reply & filters.regex("/unban_id"))
def un_ban_id(client: Client, message: Message):
    target_username = message.reply_to_message.text

    if "@" in target_username:
        target_username = target_username[1:]

    db_session = get_db().__next__()
    target_user = db_session.query(UserModel).filter(UserModel.username == target_username).first()

    if not target_user:
        message.reply(
            "This user does not exist in bot!"
        )
        return 0

    target_user.is_banned = False
    db_session.commit()

    message.reply(
        "The user has been banned from bot!"
    )