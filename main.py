"""Telegram bot that says 'Welcome {name}!'

"""
import os
import logging
import json

from telegram import User, TelegramObject, ChatMember
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ["TELEGRAM_TOKEN"]
DEBUG = os.getenv("DEBUG", False)
WELCOME_TPL = os.getenv("WELCOME_TPL", "Welcome {user_name}!")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def new_user(bot, update):
    user_name = update.message.from_user.name
    message_text = WELCOME_TPL.format(user_name=user_name)
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
    updater.idle()

if __name__ == "__main__":
    main()
