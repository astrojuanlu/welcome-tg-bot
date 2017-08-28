"""Telegram bot that says 'Welcome {name}!'

"""
import os
import logging
import json

from telegram import User, TelegramObject, ChatMember
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "445026185:AAEGtZap8RVXlVmi-9AHB_3_6gxIsJCEBi4"
WELCOME_TPL = os.getenv("WELCOME_TPL", "Welcome {user_name}!")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = log.getLogger(__name__)


def new_user(bot, update):
    user_name = update.message.from_user.name
    message_text = WELCOME_TPL.format(user_name)
    bot.sendMessage(chat_id=update.message.chat_id, text=message_text)
    bot.ChatMember(user_name)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Message for new users
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user))

    # Ignore all messages until it is called
    # TODO: Clarify this
    updater.start_polling(clean=True)

    updater.idle()

if __name__ == "__main__":
    main()
