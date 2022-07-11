from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters

from base.sql.session import get_db
from base.sql.db_methods import search_details_control
from base.plugins.searcher import google_search
from base.plugins.custom_filters import is_member_filter, ban_check_filter


# Main plugin, Search picture on google
@Client.on_message(filters.photo & filters.private & filters.create(is_member_filter) & filters.create(ban_check_filter))
def search_image(client: Client, message: Message):

    file_path = message.download()

    google_search(
        file_path,
        message
    )

    search_details_control(message.from_user.id)