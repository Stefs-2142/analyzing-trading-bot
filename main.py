from handlers_asset_add import add_start, add_step_1
from handlers_asset_add import add_step_2, add_step_3, add_step_4
from handlers_asset_del import delete_start, delete_confirm
from handlers_utils import greet_user, unknown_text, operation_cancel
from keyboards import main_shares_keyboard
from models import User, Asset
from settings import API_KEY
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler
from ticker_utils import get_ticker_price, ticker_pricing


import logging
import settings


logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    atb_bot = Updater(settings.API_KEY, use_context=True)

    dp = atb_bot.dispatcher

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Добавить'), add_start)],
        states={
            add_step_1: [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), add_step_1
                )
            ],
            add_step_2: [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), add_step_2
                 )
            ],
            add_step_3: [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), add_step_3
                )
            ],
            add_step_4: [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), add_step_4
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    ))
    dp.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Удалить'), delete_start)],
        states={
            delete_confirm: [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), delete_confirm
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    ))
    dp.add_handler(MessageHandler(Filters.text, unknown_text))

    logging.info("Bot started")
    atb_bot.start_polling()
    atb_bot.idle()


if __name__ == "__main__":
    main()
