from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters

from base.sql.session import get_db

# Main plugin, Search picture on google
@Client.on_message(filters.photo)
def search_image(client: Client, message: Message):

    db = get_db().__next__()
    user_id = update.message.from_user.id     

    google_search(
        update.message.photo[0].get_file().file_path,
        update.message
    )

    increase_search(db, user_id)