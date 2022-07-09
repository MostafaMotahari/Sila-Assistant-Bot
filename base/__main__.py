"""This file has functions for get and search an image in google
and returning the resault.
"""

# Imports
import logging
from decouple import config

from pyrogram.client import Client

from base.plugins.handlers import *
from base.sql.session import engine
from base.sql.base_class import Base
from plugins import create_local_database

PLUGIN = dict(root="base/plugins")

app = Client(
    "SilaSearch",
    api_hash=config("API_HASH"),
    api_id=config("API_ID"),
    bot_token=config("BOT_TOKEN"),
    plugins=PLUGIN
)

# Parsing bot configartion fot reading bot token
TOKEN = config['ptb']['bot_token']
updater = Updater(token=TOKEN, use_context=True, workers=24)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Dispatchers
dispatcher = updater.dispatcher

start_command_handler = CommandHandler("start", start, run_async=True)
search_photo_handler = MessageHandler(Filters.photo, search_image, run_async=True)
bot_statistics_handler = MessageHandler(Filters.user([1398458529, 5094916882]) & Filters.regex("^آمار ربات$"), bot_statistics, run_async=True)
user_statistics_handler = MessageHandler(Filters.user([1398458529, 5094916882]) & Filters.regex("^آمار کاربر$"), user_statistics, run_async=True)
public_message_handler = MessageHandler(Filters.user([1398458529, 5094916882]) & Filters.regex("^پیام همگانی$"), public_message, run_async=True)
signup_user_by_admin = MessageHandler(Filters.user([1398458529, 5094916882]) & Filters.regex("Id: "), signup_by_admin, run_async=True)


dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(search_photo_handler)
dispatcher.add_handler(bot_statistics_handler)
dispatcher.add_handler(user_statistics_handler)
dispatcher.add_handler(public_message_handler)
dispatcher.add_handler(signup_user_by_admin)


# Running bot
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    create_local_database()
    app.run()
