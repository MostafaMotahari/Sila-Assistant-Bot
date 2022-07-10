import requests
from time import sleep
from html import escape
import json

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

import base.sql.session as session
from base.sql.db_methods import get_users_list

# Parsing bot configartion fot reading bot token
config = configparser.ConfigParser()
config.read("base/config.ini")
TOKEN = config['ptb']['bot_token']
API_URL = config['api']['api_url']
print(API_URL)

#Function that gives a page html content
def google_search(file_path, message):
    
    img_url = file_path
    msg = message.reply_text("🔎 *در حال زدن...*", parse_mode="Markdown")
    
    # Get search page
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14', 
    #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-language': 'en-US,en;q=0.9'}

    # The required data and headers for sending to api
    data = {
        "image_url": img_url,
        "resized_images": False,
        "cloud_api": False
    }

    headers = {'Content-type': 'application/json'}

    # Request to api
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    # Parse all needed information
    j = response.json()

    # Try parse suggestion
    try:
        suggestion = j["best_guess"]
    except Exception as e:
        print(e, "No suggestion")
        suggestion = False

    # Try parse similar
    #try:
    #    find_similar = b.select(".e2BEnf")
    #    similar = 'https://www.google.com' + str(find_similar[0].a['href'])
    #except Exception as e:
    #    print(e, "No similar")
    #    similar = False

    # Try parse sites
    try:
        sites = [(link, site) for site, link in zip(j["titles"], j["links"])]
    except Exception as e:
        print(e, "No sites")
        sites = False

    # Send
    txt = ''
    if suggestion:
        txt = '<b>Main suggestion: %s</b>\n\n' % escape(suggestion)

    txt += '<b>Search results:</b>\n\n'
    if sites:
        txt += '\n\n'.join([f'<a href="{escape(site[0])}">{escape(site[1])}</a>' for site in sites])

    inline_keyboard = []
    #if similar:
    #    inline_keyboard.append([
    #        InlineKeyboardButton(text="🔗 Link to similar images", url=similar)
    #    ])

    inline_keyboard.append([
        InlineKeyboardButton(text="🌐 Search page", url="https://www.google.com/searchbyimage?image_url=" + img_url)
    ])
    msg.edit_text(text=txt, parse_mode='html', reply_markup=InlineKeyboardMarkup(inline_keyboard), disable_web_page_preview=True)


# Creating a local database for temporary requests
def create_local_database():
    db = session.get_db().__next__()

    for user_id in get_users_list(db):
        session.TEMP_DATA.append(user_id)
