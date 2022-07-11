import site
import requests
from html import escape
import bs4
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from base.plugins import message_templates

# Selenium static variables
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
options = Options()
options.headless = True

#Function that gives a page html content
def google_search(file_path: str, message: Message):
    
    search_result_msg: Message = message.reply("**Searching ...**")
    
    # Get search page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14', 
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-language': 'en-US,en;q=0.9'}
    searchUrl = 'http://www.google.hr/searchbyimage/upload'
    multipart = {'encoded_image': (file_path, open(file_path, 'rb')), 'image_content': ''}

    response = requests.post(searchUrl, headers=headers, files=multipart, allow_redirects=False)

    # Parse all needed information
    b = bs4.BeautifulSoup(response.text, "html.parser")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    driver.get(b.a["href"])
    b = bs4.BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Try parse suggestion
    try:
        find_sug = b.select('.fKDtNb')
        suggestion = find_sug[0].text
    except Exception as e:
        print(e, "No suggestion")
        suggestion = False

    # Try parse similar
    try:
        find_similar = b.select(".e2BEnf")
        similar = 'https://www.google.com' + str(find_similar[0].a['href'])
    except Exception as e:
        print(e, "No similar")
        similar = False

    # Try parse sites
    try:
        find_sites = b.find_all('div', {'class': 'yuRUbf'})
        sites = [(si.a['href'], si.h3.text) for si in find_sites]
    except Exception as e:
        print(e, "No sites")
        sites = False

    # Set search result text
    text = message_templates.search_result_message_template.format(
        escape(suggestion) if suggestion else "No main results.",
        "\n\n".join([f"[{escape(site[1])}]({escape(site[0])})" for site in sites]) if sites else "No sites."
    )

    # Add inline keyboards
    inline_keyboard = []
    if similar:
        inline_keyboard.append([
            InlineKeyboardButton(text="🔗 Link to similar images", url=similar)
        ])

    # Apply the results.
    search_result_msg.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard),
        disable_web_page_preview=True
    )
