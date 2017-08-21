""" Bot para el grupo Python_Cientifico """

from telegram import User, TelegramObject, ChatMember
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging as log
import json

TOKEN = "445026185:AAEGtZap8RVXlVmi-9AHB_3_6gxIsJCEBi4"

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = log.getLogger(__name__)

#---------Funciones del bot---------------
def new_user(bot, update):
    user_name = update.message.from_user.name
    mensaje = ("Bienvenido %s al grupo de Python Científico, aquí podrás compartir cosas sobre" % str(user_name) +
               "Todo el entorno cientifico de este gran lenguaje")
    bot.sendMessage(chat_id=update.message.chat_id, text=mensaje)
    bot.ChatMember(user_name)

def normas(bot, update):
    user_name = update.message.from_user.name
    ChatMember("Estas son las normas bla bla")


def help(bot, update):
    user_name = update.message.from_user.name
    mensaje = ("Estoy aquí para ayudarte %s") %str(user_name)
    bot.sendMessage(chat_id=update.message.chat_id, text=mensaje)


# Test del bot pero con POO
#
# class Bot(object):
#     def __init__(self, bot, update):
#         self.user_name = update.message.from_user.name
#
#
#     def new_user(self, bot, update):
#         bot.sendMessage("Bienvenido %s al grupo de Python Científico, aquí podrás compartir cosas sobre" % str(self.user_name) +
#                                    "Todo el entorno cientifico de este gran lenguaje")
#
#     def normas(self, bot, update):
#         telegram.User.ChatMember(self.user_name, "Estas son las normas bla bla")
#
#     def help(self, bot, update):
#         bot.sendMessage("Estoy aquí para ayudarte %s") %str(self.user_name)

#--------------COMANDOS--------------

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("normas" or "Normas", normas))

    # Mensaje para los nuevos usuarios
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_user))

    # Ignora todos los mensajes hasta que se le llama
    updater.start_polling(clean=True)

    updater.idle()

if __name__ == "__main__":
    main()
