from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message
from decouple import config

from base.sql.session import get_db
from base.sql.models import UserModel

@Client.on_message(filters.private & filters.regex("^/add (.*)$") & filters.user(config("OWNER")))
def increase_credit(client: Client, message: Message):
    credit_amount = message.text.split(" ")[1]
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

    target_user.search_credit += int(credit_amount)
    db_session.commit()

    message.reply(f"➕ {credit_amount} searches has been added to {target_username} credit!")
