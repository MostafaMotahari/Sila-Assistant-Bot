"""This file has functions for get and search an image in google
and returning the resault.
"""

# Imports
from decouple import config
from pyrogram.client import Client

from base.sql.session import engine
from base.sql.base_class import Base
from base.sql.db_methods import migrations

PLUGIN = dict(root="base/plugins")

app = Client(
    "SilaSearch",
    api_hash=config("API_HASH"),
    api_id=config("API_ID"),
    bot_token=config("BOT_TOKEN"),
    plugins=PLUGIN
)

# Running bot
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    migrations()
    app.run()
