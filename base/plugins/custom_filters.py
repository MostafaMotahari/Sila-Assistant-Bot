import json

import requests
from decouple import config
from pyrogram.types import Message, User

from base.sql.db_methods import check_user_exist, add_user, get_user
from base.plugins import message_templates

# Check joining in daatabase
def check_joining_db(user: User, username: str):
    headers = {'Authorization': f'Token {config("API_TOKEN")}'}
    response = requests.get(f'{config("API_URL")}/users/?username={username}', headers=headers)
    response: dict = json.loads(response.text)

    if len(response) != 0:
        if response.get("team", None):
            add_user(
                user,
                is_admin= True if response["is_admin"] == True else False,
                is_superuser= True if response["is_superuser"] == True else False
            )
            return True
        return False

    return False


# Is memeber filters
def is_member_filter(_, __, message: Message):
    if not check_user_exist(message.from_user.id):
        if check_joining_db(message.from_user, message.from_user.username):
            return True
        message.reply(message_templates.not_member_message_template)
        return False
    return True


# Ban check filter
def ban_check_filter(_, __, message: Message):
    if not get_user(message.from_user.id).is_banned:
        return True
    message.reply(message_templates.ban_user_message_template)
    return False