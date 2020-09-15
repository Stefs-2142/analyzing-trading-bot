import logging
import telegram
from telegram.utils.request import Request

from handlers_binance_calls import get_balance
from handlers_binance_set_order import set_order, choosing_order_type
from handlers_binance_set_order import choosing_pair, choosing_order_side
from handlers_binance_set_order import prepearing_order, making_order, checking_price
from handlers_binance_get_price import get_price, getting_pair_price, getting_another_pair
from handlers_open_orders import get_open_orers
from handlers_close_order import choosing_order_for_close, applying_closing, closing_order

from handlers_orders_history import get_trade_history, prepearing_trade_history

from handlers_asset_add import add_start, add_step_1
from handlers_asset_add import add_step_2, add_step_3, add_step_4
from handlers_asset_edit_del import (
    edit_delete_start, delete_price_choose, edit_delete_choose,
    edit_choose_confirm, edit_price
)
from handlers_asset_view import asset_view
from handlers_utils import (
    greet_user, unknown_text, operation_cancel, show_help,
    shares_comands, binance_comands
)

from settings import TELEGRAM_API_KEY
from tasks import polling
from telegram.ext import (
    Updater, CommandHandler,
    MessageHandler, Filters, ConversationHandler
)

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():

    request = Request(con_pool_size=8)
    bot = telegram.Bot(TELEGRAM_API_KEY, request=request)

    atb_bot = Updater(bot=bot, use_context=True)
    dp = atb_bot.dispatcher

    assets = ConversationHandler(
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
    )

    edit_asssets = ConversationHandler(
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
    )

    price = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Текущий курс'), get_price)],
        states={
            "get_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), getting_pair_price
                )
            ],
            "get_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), getting_another_pair
                )
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    )

    orders = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Создать ордер'), set_order)],
        states={
            "set_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), choosing_pair
                )
            ],
            "set_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), choosing_order_type
                )
            ],
            "set_step_3": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), choosing_order_side
                )
            ],
            "set_step_4": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), checking_price
                )
            ],
            "set_step_5": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), prepearing_order
                )
            ],
            "set_step_6": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), making_order
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    )

    close_order = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Отменить ордер'), choosing_order_for_close)],
        states={
            "close_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), applying_closing
                )
            ],
            "close_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), closing_order
                )
            ],


        },
        fallbacks=[MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    )

    pair_trade_history = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('История торгов'), get_trade_history)],
        states={
            "history_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), prepearing_trade_history
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('(Отмена)'), operation_cancel)]
    )

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.regex('Меню Binance'), binance_comands))
    dp.add_handler(MessageHandler(Filters.regex('Меню акций'), shares_comands))
    dp.add_handler(MessageHandler(Filters.regex('Узнать баланс'), get_balance))
    dp.add_handler(MessageHandler(Filters.regex('Мои инструменты'), asset_view))
    dp.add_handler(MessageHandler(Filters.regex('Помощь'), show_help))
    dp.add_handler(MessageHandler(Filters.regex('Открытые ордеры'), get_open_orers))

    dp.add_handler(assets)
    dp.add_handler(edit_asssets)
    dp.add_handler(price)
    dp.add_handler(orders)
    dp.add_handler(close_order)
    dp.add_handler(pair_trade_history)

    dp.add_handler(MessageHandler(Filters.text, unknown_text))

    logging.info("Bot started")
    atb_bot.start_polling()
    polling.delay()

    atb_bot.idle()


if __name__ == "__main__":
    main()
