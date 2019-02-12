"""Telegram bot for welcome

"""
import os
import re
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ["TELEGRAM_TOKEN"]
PORT = int(os.environ["PORT"])


MSG = "¡Te damos la bienvenida {}! En el mensaje anclado están las reglas básicas del grupo."
TIMEOUT = 600  # in seconds

URI_MAIL = r'[/@]WORD(\.WORD)'.replace('WORD', '[^\s.]+')
BAN_RULES = (
    (lambda name: len(name) > 30, "id={} member in id={} group ban by: long name"),
    (re.compile(URI_MAIL).search, "id={} member in id={} group ban by: name with url/uri/email"),
)
NOT_BAN_MSG = "id={} member in id={} group can not ban: {}"
GREET_FROM_MEMBERS = re.compile("[bv]ien[vb]enid|welcome", re.IGNORECASE).search


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


def send_greeting(bot, job):
    # Users must have first_name, last_name or username to be greeted
    chat_id, chat_data = job.context
    user_list = ', '.join(u for u in chat_data['users_to_greet'].values() if u)
    if user_list:
        bot.send_message(chat_id, text=MSG.format(user_list))
        not_greet_user(chat_data)


def delete_job(chat_data):
    if 'job' in chat_data:
        job = chat_data['job']
        job.schedule_removal()
        del chat_data['job']


def not_greet_user(chat_data, user_id=None):
    # user_id=None do not greet anyone
    if 'users_to_greet' in chat_data:
        if user_id:
            chat_data['users_to_greet'].pop(user_id, None)
        else:
            chat_data['users_to_greet'].clear()


def new_user(bot, update, job_queue, chat_data):
    if 'users_to_greet' not in chat_data:
        chat_data['users_to_greet'] = {}

    new_users = False
    for user in (update.message.new_chat_members or [update.message.from_user]):
        name = user.first_name or user.last_name or user.username or ""
        greet = True
        if name:
            for rule, reason in BAN_RULES:
                if rule(name):
                    ban_member(bot, update, user, reason)
                    greet = False
                    break
        if greet and not user.is_bot:
            chat_data['users_to_greet'][user.id] = name
            new_users = True

    if new_users:
        # Resetting the waiting time
        delete_job(chat_data)
        # New countdown
        job = job_queue.run_once(send_greeting, TIMEOUT, context=(update.message.chat_id, chat_data))
        chat_data['job'] = job


def bye_user(bot, update, chat_data):
    not_greet_user(chat_data, update.message.left_chat_member.id)
    if update.message.from_user.id == bot.id:
        update.message.delete()  # left_chat_member messages from kick


def conversation(bot, update, chat_data):
    if GREET_FROM_MEMBERS(update.message.text):
        delete_job(chat_data)
        not_greet_user(chat_data)


def error(bot, update, error):
    logger.warning('Update "{}" caused error "{}"'.format(update, error))


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                  new_user,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,
                                  bye_user,
                                  pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.group,
                                  conversation,
                                  pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Ignore all messages until it is called
    #updater.start_polling(clean=True)

    # Wait for termination
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://bienvenida-es-bot.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == "__main__":
    main()
