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

URI_MAIL = r'[/@]WORD(\.WORD)'.replace('WORD', '[^\s.]+')
BAN_RULES = (
    (lambda name: len(name) > 30, "id={} member ban by: long name"),
    (re.compile(URI_MAIL).search, "id={} member ban by: name with url/uri/email"),
)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def ban_member(bot, update, user):
    chat_id = update.message.chat_id
    user_id = user.id

    kicked = bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
    if kicked:
        catheter = bot.sendMessage(chat_id=chat_id, text="Member kicked")

        id1 = update.message.message_id  # Identification of the join message
        id3 = catheter.message_id        # Identification of the catheter message :)
        id2 = id3 - 1                    # Identification of the kicked message (potential)

        for i in range(id2, id1, -1):
            # Reply
            m = bot.sendMessage(chat_id=chat_id, text="reply", reply_to_message_id=i)
            l = m.reply_to_message.left_chat_member
            if l and l.id == user_id:
                # Kicked message!
                bot.delete_message(chat_id=chat_id, message_id=m.reply_to_message.message_id)
            # Delete reply message
            bot.delete_message(chat_id=chat_id, message_id=m.message_id)

        # Delete join and catheter messages
        bot.delete_message(chat_id=chat_id, message_id=id1)
        bot.delete_message(chat_id=chat_id, message_id=id3)
    else:
        logger.error("The id={} member could not be banned".format(user_id))


def new_user(bot, update):
    message_texts = []
    for user in (update.message.new_chat_members or [update.message.from_user]):
        name = user.first_name or user.last_name or user.username
        greet = True
        if name:
            for rule, reason in BAN_RULES:
                if rule(name):
                    ban_member(bot, update, user)
                    logger.debug(reason.format(user.id))
                    greet = False
                    break
            else:
                name = ", {}".format(name)
        else:
            name = ""
        if greet and not user.is_bot:
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
