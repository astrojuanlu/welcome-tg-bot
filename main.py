""" Bot para el grupo Python_Cientifico """

from telegram import User, TelegramObject
from telegram.ext import Updater, CommandHandler, MessageHandler
import logging as log
import json

TOKEN = "TOKEN"

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

#---------Funciones del bot---------------
def new_user(bot, update):
    user_name = update.message.from_user.name
    bot.sendMessage("Bienvenido %s al grupo de Python Científico, aquí podrás compartir cosas sobre" % str(user_name) +
                    "Todo el entorno cientifico de este gran lenguaje")

def normas(bot, update):
    user_name = update.message.from_user.name
    telegram.User.ChatMember("Estas son las normas bla bla")


def help(bot, update):
    user = update.message.from_user.name
    string = ("Estoy aquí para ayudarte %s") %str(user_name)

    bot.sendMessage(string)

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

dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("normas", normas))

# Mensaje para los nuevos usuarios
dispatcher.add_handler(MessageHandler(Filers.status_update.new_chat_members, new_user))

# Ignora todos los mensajes hasta que se le llama
updater.start_polling(clean=True)

updater.idle()
