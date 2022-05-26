
# Google reverse image search bot



![GitHub](https://img.shields.io/github/license/MostafaMotahari/Google-Reverse-Search-by-Image?style=flat-square)
![Logo](https://raw.githubusercontent.com/MostafaMotahari/Google-Reverse-Search-by-Image/master/images/google-reverse-image-search-bot.png)


## Introductions

**Search Engine:** Google

**Modules:** Pyrogram, SQLAlchemy

Simple telegram bot that scraps search data from google search engine and returns as a telegram message.

Also It also **stores users' search statistics with a very good structure in a SQL database**.
## Installation

To install this project on your personal server, first od all clone this repo

```bash
  git clone https://github.com/MostafaMotahari/Google-Reverse-Search-by-Image.git
```
    
Then run these commands
```bash
  cd Google-Reverse-Search-by-Image
  pip install requirements.txt
```

And finally run the project
```bash
  python -m base
```
## Some Notes

Recently, Google imposed restrictions on Data Scrapers that may cause the bot to malfunction.

This problem may be observed in changing the class of div tags, in which case the process of scraping the data is not done properly.

In this case you need to manually change the classes in ```base/plugin.py``` the file.

