import json

import requests
from decouple import config
from pyrogram.types import Message

from base.sql.db_methods import check_user_exist

# Check joining in daatabase
def check_joining_db(username: str):
    headers = {'Authorization': f'Token {config("API_TOKEN")}'}
    response = requests.get(f'{config("API_URL")}/users/?username={username}', headers=headers)
    response: dict = json.loads(response.text)[0]

    if response.get("team", None):
        return True

    return False


# Is memeber filters
def is_member_filter(_, __, message: Message):
    if check_user_exist(message.from_user.id) or check_joining_db(message.from_user.username):
        return True
    return False