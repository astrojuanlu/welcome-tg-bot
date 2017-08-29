"""Telegram bot that says 'Welcome {name}!'

"""
import os
import logging
import json

import requests

from telegram import User, TelegramObject, ChatMember
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ["TELEGRAM_TOKEN"]
DEBUG = os.getenv("DEBUG", False)
LANG = os.getenv("LANGUAGE", "es_ES")[:2]
PORT = int(os.getenv("PORT", "5000"))

GENDERIZE_URL = "https://api.genderize.io/?name={name}&language_id={lang}"

WELCOME_MESSAGES = {
    'male': '¡Bienvenido {user_name}!',
    'female': '¡Bienvenida {user_name}!',
}

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_gender(name, default="male", language=LANG):
    resp = requests.get(GENDERIZE_URL.format(
        name=name, lang=language)).json()
    gender = (resp.get("gender") or default).lower()
    return gender

def new_user(bot, update):
    user_name = update.message.from_user.name
    message_tpl = WELCOME_MESSAGES[get_gender(user_name)]
    message_text = message_tpl.format(user_name=user_name)
    bot.sendMessage(chat_id=update.message.chat_id, text=message_text)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Message for new users
    if DEBUG:
        dp.add_handler(CommandHandler('start', start))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user))

    # Ignore all messages until it is called
    updater.start_polling(clean=True)

    # Wait for termination
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://bienvenida-es-bot.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == "__main__":
    main()
