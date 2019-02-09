"""Telegram bot for welcome

"""
import os
import re
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ["TELEGRAM_TOKEN"]
PORT = int(os.environ["PORT"])

MSG = "¡Te damos la bienvenida{}! En el mensaje anclado tienes las reglas básicas del grupo."

URI_MAIL = r'[/@]WORD(\.WORD)'.replace('WORD', '[^\s.]+')
BAN_RULES = (
    (lambda name: len(name) > 30, "id={} member in id={} group ban by: long name"),
    (re.compile(URI_MAIL).search, "id={} member in id={} group ban by: name with url/uri/email"),
)
NOT_BAN_MSG = "id={} member in id={} group can not ban: {}"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def ban_member(bot, update, user, reason):
    chat = update.message.chat

    all_adm = chat.all_members_are_administrators
    bot_adm = any(m.user.id == bot.id for m in chat.get_administrators())

    if bot_adm and not all_adm:
        kicked = chat.kick_member(user_id=user.id)
        if kicked:
            update.message.delete()  # new_chat_members messages
            logger.debug(reason.format(user.id, chat.id))
        else:
            cause = "unknown"
            logger.debug(NOT_BAN_MSG.format(user.id, chat.id, cause))
    else:
        cause = "requirements are not met"
        logger.debug(NOT_BAN_MSG.format(user.id, chat.id, cause))


def new_user(bot, update):
    message_texts = []
    for user in (update.message.new_chat_members or [update.message.from_user]):
        name = user.first_name or user.last_name or user.username or ""
        greet = True
        if name:
            for rule, reason in BAN_RULES:
                if rule(name):
                    ban_member(bot, update, user, reason)
                    greet = False
                    break
            else:
                name = ", {}".format(name)
        if greet and not user.is_bot:
            message_texts.append(MSG.format(name))
    if message_texts:
        update.message.chat.send_message(text='\n'.join(message_texts))


def bye_user(bot, update):
    if update.message.from_user.id == bot.id:
        update.message.delete()  # left_chat_member messages from kick


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, bye_user))

    # Ignore all messages until it is called
    #updater.start_polling(clean=True)

    # Wait for termination
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://bienvenida-es-bot.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == "__main__":
    main()
