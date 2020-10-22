import logging
import telegram
from telegram.utils.request import Request

from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters)

from settings import TELEGRAM_API_KEY

from conversations import (assets, edit_asssets,
                           edit_crypto_asssets, price, crypto_assets,
                           orders, close_order, pair_trade_history)

from handlers.binance_calls import get_balance

from handlers.open_orders import get_open_orers

from handlers.asset_view import asset_view

from handlers.utils import (greet_user, unknown_text, show_help,
                            shares_comands, binance_comands,
                            back_to_menu, crypto_shares_comands)

from handlers.crypto_asset_view import crypto_asset_view

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():

    request = Request(con_pool_size=8)
    bot = telegram.Bot(TELEGRAM_API_KEY, request=request)

    atb_bot = Updater(bot=bot, use_context=True)
    dp = atb_bot.dispatcher

    dp.add_handler(assets)
    dp.add_handler(edit_asssets)
    dp.add_handler(edit_crypto_asssets)
    dp.add_handler(price)
    dp.add_handler(orders)
    dp.add_handler(close_order)
    dp.add_handler(pair_trade_history)
    dp.add_handler(crypto_assets)

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('Меню Binance'), binance_comands))
    dp.add_handler(MessageHandler(Filters.regex('Меню акций'), shares_comands))
    dp.add_handler(MessageHandler(Filters.regex('Узнать баланс'), get_balance))
    dp.add_handler(MessageHandler(Filters.regex('Мои инструменты'), asset_view))
    dp.add_handler(MessageHandler(Filters.regex('Помощь'), show_help))
    dp.add_handler(MessageHandler(Filters.regex('Открытые ордеры'), get_open_orers))
    dp.add_handler(MessageHandler(Filters.regex('Уведомления'), crypto_shares_comands))
    dp.add_handler(MessageHandler(Filters.regex('Отслеживаемые'), crypto_asset_view))
    dp.add_handler(MessageHandler(Filters.regex('Назад'), back_to_menu))

    dp.add_handler(MessageHandler(Filters.text, unknown_text))

    logging.info("Bot started")
    atb_bot.start_polling()
    atb_bot.idle()


if __name__ == "__main__":
    main()
