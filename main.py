from handlers_utils import greet_user, unknown_text
from model import DbUtils
from settings import API_KEY
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler

import logging
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO)

def main():
    atb_bot = Updater(settings.API_KEY, use_context=True)
    
    dp = atb_bot.dispatcher
    
    # Объявление диспетчера и описание хендлеров
    dp = atb_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    # dp.add_handler(ConversationHandler(
    #     entry_points = [CommandHandler("cities", cities_start)],
    #     states = {cities_in_progress:[MessageHandler(Filters.text, cities_in_progress)]},
    #     fallbacks = [CommandHandler("cancel", cancel)]
    # ))
    dp.add_handler(MessageHandler(Filters.text, unknown_text))
    
    # Запускаем апдейтер и пишем это в лог
    logging.info("Bot started")
    atb_bot.start_polling()
    atb_bot.idle()
    # db = DbUtils()
    # users = db.GetUsers()
    # for user in users:
    #     print(user)


if __name__ == "__main__":
    main()
