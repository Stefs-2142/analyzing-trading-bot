import logging
import settings
import telegram


from handlers_binance_calls import binance_comands, get_balance

from handlers_asset_add import add_start, add_step_1
from handlers_asset_add import add_step_2, add_step_3, add_step_4
from handlers_asset_edit_del import (
    edit_delete_start, delete_price_choose, edit_delete_choose,
    edit_choose_confirm, edit_price
)
from handlers_asset_view import asset_view
from handlers_utils import (
    greet_user, unknown_text, operation_cancel, show_help,
    shares_comands
)
from keyboards import main_shares_keyboard
from models import User, Asset
from settings import TELEGRAM_API_KEY
from tasks import polling
from telegram.ext import (
    Updater, CommandHandler,
    MessageHandler, Filters, ConversationHandler
)
from ticker_utils import get_ticker_price, ticker_pricing


logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
    'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def main():
    bot = telegram.Bot(TELEGRAM_API_KEY)

    atb_bot = Updater(bot=bot, use_context=True, request_kwargs=PROXY)

    dp = atb_bot.dispatcher

    dp.add_handler(CommandHandler("start", greet_user))

    dp.add_handler(
        MessageHandler(Filters.regex('Меню\sBinance'), binance_comands)
    )

    dp.add_handler(
        MessageHandler(Filters.regex('Меню\sакций'), shares_comands)
    )

    dp.add_handler(
        MessageHandler(Filters.regex('Узнать\sбаланс'), get_balance)
    )

    dp.add_handler(
        MessageHandler(Filters.regex('Мои\sинструменты'), asset_view)
    )
    dp.add_handler(MessageHandler(Filters.regex('Помощь'), show_help))

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
        entry_points=[MessageHandler(
            Filters.regex('Изменить/Удалить'), edit_delete_start
        )],
        states={
            delete_price_choose: [
                MessageHandler(
                    Filters.regex('Изменить|Удалить'), delete_price_choose
                )
            ],
            edit_delete_choose: [
                MessageHandler(
                    Filters.text & (
                        ~Filters.regex('(Отмена|Изменить|Удалить)')
                    ), edit_delete_choose
                )
            ],
            edit_choose_confirm: [
                MessageHandler(
                    Filters.text & (
                        ~Filters.regex('(Отмена|Изменить|Удалить)')
                    ), edit_choose_confirm
                )
            ],
            edit_price: [
                MessageHandler(
                    Filters.text & (
                        ~Filters.regex('(Отмена|Изменить|Удалить)')
                    ), edit_price
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    ))

    dp.add_handler(MessageHandler(Filters.text, unknown_text))

    logging.info("Bot started")
    atb_bot.start_polling()
    polling.delay()

    atb_bot.idle()


if __name__ == "__main__":
    main()
