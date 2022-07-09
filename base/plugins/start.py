from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram import filters

from base.plugins import message_templates

# Send start message
@Client.on_message(filters.regex("^/start$") & filters.private)
def start(client: Client, message: Message):
    message.reply(message_templates.start_message_template)
