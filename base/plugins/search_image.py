from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters

from base.sql.session import get_db
from base.sql.db_methods import search_details_control
from base.plugins.searcher import google_search

# Main plugin, Search picture on google
@Client.on_message(filters.photo & filters.private)
def search_image(client: Client, message: Message):

    db = get_db().__next__()
    file_path = message.download()

    google_search(
        file_path,
        message
    )

    search_details_control(db, message.from_user.id)