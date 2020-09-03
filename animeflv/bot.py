import telebot
import sys
import textwrap
import random
import os
from pathlib import Path

from .api import search_anime, find_details, download_one


bot = telebot.TeleBot(token=sys.argv[1])
bot.mappings = {}
bot.reverse_mappings = {}


def add_mapping(url):
    if url in bot.reverse_mappings:
        return bot.reverse_mappings[url]

    string = "".join(random.choice("abcdefghijklnmopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(16))
    bot.mappings[string] = url
    bot.reverse_mappings[url] = string

    return string


@bot.message_handler(["start", "help"])
def send_welcome(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        textwrap.dedent(
            """
        Hello! I will help you search for and download videos from AnimeFLV.net
        
        Send me any query and I will return you a list of matching titles from AnimeFLV.
        """,
        ),
        disable_web_page_preview=True,
    )


@bot.message_handler(regexp=r"/anime_[a-zA-Z]+")
def anime_info(message: telebot.types.Message):
    string = message.text[len("/anime_"):]

    if string not in bot.mappings:
        bot.reply_to(message, "❌ Unknown ID. Try searching again.")
        return

    url = bot.mappings[string]
    total_chapters, description = find_details(url)

    if description:
        bot.send_message(message.chat.id, description)

    bot.send_message(
        message.chat.id,
        f"""Here is the list of all chapters. 
Click any link to start downloading that file. 
The file will be split in 50 MBs parts as per Telegram's restrictions.
        """,
    )

    chapters = "\n".join(f"🔸 {i+1}: /video_{string}_{i+1}" for i in range(total_chapters))
    bot.send_message(message.chat.id, chapters)


@bot.message_handler(regexp=r"/video_[a-zA-Z]+_\d+")
def download_video(message: telebot.types.Message):
    string, chapter = message.text[len("/video_"):].split("_")

    if string not in bot.mappings:
        bot.reply_to(message, "❌ Unknown ID. Try searching again.")
        return

    bot.send_message(message.chat.id, "🔽 Downloading video file from AnimeFLV.net")

    url = bot.mappings[string]
    path = download_one(url, chapter, ".")

    os.system(f"MP4Box -splits 50000 {path}")
    parts = list(sorted(Path(".").glob(str(path.stem) + "_*.mp4")))

    bot.send_message(message.chat.id, f"🔼 Uploading {len(parts)} video file(s) to Telegram")

    for fname in parts:
        with fname.open("rb") as fp:
            bot.send_chat_action(message.chat.id, "upload_video")
            bot.send_document(message.chat.id, fp)
            fname.unlink()

    path.unlink()
    bot.send_message(message.chat.id, "👌 Done!")


@bot.message_handler(func=lambda _: True)
def query(message: telebot.types.Message):
    items = search_anime(message.text, find_details=False)
    titles = "\n".join(f"🔹 {item}\n      /anime_{add_mapping(url)}" for item, (url, _) in items.items())

    bot.send_message(
        message.chat.id,
        f"""Here is a list of matching titles. Click the corresponding link to see the description and chapters.
        
{titles}
        """,
    )


bot.polling(none_stop=True)
