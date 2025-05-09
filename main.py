from urllib.parse import urlparse
import datetime
import telebot
import config
import yt_dlp
import re
import os
from telebot import types
from telebot.util import quick_markup
import time

bot = telebot.TeleBot(config.token)
last_edited = {}

def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match
    return youtube_regex_match

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أرسل رابط فيديو من يوتيوب وسأقوم بتحميله لك.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if youtube_url_validation(url):
        msg = bot.reply_to(message, "جارٍ التحميل...")
        try:
            ydl_opts = {
                'format': 'best[filesize<49M]/best',
                'outtmpl': 'video.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)
                with open(file_name, 'rb') as f:
                    bot.send_video(message.chat.id, f, caption=info.get("title", "الفيديو"))
                os.remove(file_name)
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ: {str(e)}")
    else:
        bot.reply_to(message, "هذا الرابط غير صالح أو لا يخص يوتيوب.")

bot.infinity_polling()