"""Telegram bot for welcome

"""
import os
import re
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ["TELEGRAM_TOKEN"]
DEBUG = os.getenv("DEBUG", False)
PORT = int(os.environ["PORT"])

MSG = "¡Te damos la bienvenida{}! En el mensaje anclado tienes las reglas básicas del grupo."

URI_MAIL = r'(\w+:)?(//\w+(\.\w+)+(/[^\s]*)?|[\w.+-]+@\w+(\.\w+)+)'
IGNORE_RULES = (
    (lambda name: len(name) > 30, "User ignored by: long name"),
    (re.compile(URI_MAIL).search, "User ignored by: name with url/uri/email"),
)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def new_user(bot, update):
    message_texts = []
    for user in (update.message.new_chat_members or [update.message.from_user]):
        if not user.is_bot:  # new in v8.0
            name = user.first_name or user.last_name or user.username
            ignore = False
            if name:
                for rule, reason in IGNORE_RULES:
                    if rule(name):
                        logger.debug(reason)
                        ignore = True
                        break
                name = ", {}".format(name)
            else:
                name = ""
            if not ignore:
                message_texts.append(MSG.format(name))
    if message_texts:
        bot.sendMessage(chat_id=update.message.chat_id, text='\n'.join(message_texts))

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
    #updater.start_polling(clean=True)

    # Wait for termination
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://bienvenida-es-bot.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == "__main__":
    main()
