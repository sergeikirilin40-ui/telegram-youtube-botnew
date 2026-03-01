import os
import uuid
import telebot
from telebot import types
import yt_dlp

TOKEN = os.getenv("TOKEN") or "8731518379:AAFpR8wrGvMR1HOYLYkf9cVAWbUAw28Nzl4"

bot = telebot.TeleBot(TOKEN)

TEMP_DIR = "downloads"
os.makedirs(TEMP_DIR, exist_ok=True)

user_format = {}

@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("mp4", "mp3")
    bot.send_message(
        message.chat.id,
        "Привет 👋\nВыбери формат, потом пришли ссылку на YouTube",
        reply_markup=kb
    )

@bot.message_handler(func=lambda m: m.text in ["mp4", "mp3"])
def choose_format(message):
    user_format[message.chat.id] = message.text
    bot.send_message(
        message.chat.id,
        f"Формат выбран: {message.text}\nТеперь пришли ссылку",
        reply_markup=types.ReplyKeyboardRemove()
    )

@bot.message_handler(func=lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
def download(message):
    chat_id = message.chat.id

    if chat_id not in user_format:
        bot.send_message(chat_id, "Сначала выбери mp4 или mp3")
        return

    fmt = user_format[chat_id]
    uid = str(uuid.uuid4())

    bot.send_message(chat_id, "⏳ Скачиваю...")

    try:
        if fmt == "mp4":
            out = f"{TEMP_DIR}/{uid}.mp4"
            ydl_opts = {
                "outtmpl": out,
                "format": "best[ext=mp4]/best"
            }
        else:
    out = f"{TEMP_DIR}/{uid}.mp3"

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])

        with open(out, "rb") as f:
            bot.send_document(chat_id, f)

        os.remove(out)

    except Exception as e:
        bot.send_message(chat_id, f"Ошибка 😢\n{e}")


bot.infinity_polling(timeout=10, long_polling_timeout=5)

