import logging
import telegram
from telegram.utils.request import Request

from handlers.binance_calls import get_balance

from handlers.binance_set_order import (
    set_order, choosing_order_type,
    choosing_pair, choosing_order_side,
    prepearing_order, making_order, checking_price
)

from handlers.binance_get_price import get_price, getting_pair_price, getting_another_pair_price

from handlers.open_orders import get_open_orers

from handlers.close_order import choosing_order_for_close, applying_closing, closing_order

from handlers.orders_history import get_trade_history, prepearing_trade_history
from handlers.orders_history import getting_another_pair_orders

from handlers.crypto_asset_add import (
    add_crypto, choosing_pair_for_target,
    checking_price_for_target, aplying_target
)

from handlers.asset_add import (
    add_start, add_step_1,
    add_step_2, add_step_3, add_step_4
)

from handlers.asset_edit_del import (
    edit_delete_start, delete_price_choose, edit_delete_choose,
    edit_choose_confirm, edit_price
)

from handlers.asset_view import asset_view

from handlers.utils import (
    greet_user, unknown_text, operation_cancel, show_help,
    shares_comands, binance_comands, crypto_shares_comands,
    back_to_menu
)

from handlers.crypto_asset_view import crypto_asset_view

from handlers.crypto_asset_edit_del import (
    edit_delete_choose_crypto,
    edit_delete_start_crypto, delete_price_choose_crypto,
    edit_choose_confirm_crypto, edit_price_crypto
)

from settings import TELEGRAM_API_KEY

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
        entry_points=[MessageHandler(Filters.regex('Добавить'), add_start),],
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
        entry_points=[MessageHandler(Filters.regex('Изменить/Удалить'), edit_delete_start)],
        states={
            '1': [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), edit_delete_choose
                )
            ],
            '2': [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), delete_price_choose
                )
            ],
            '3': [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), edit_choose_confirm
                )
            ],
            '4': [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), edit_price
                )
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex('(Отмена)'), operation_cancel),
            MessageHandler(Filters.regex('(Назад)'), back_to_menu)
        ]
    )

    edit_crypto_asssets = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Edit/Delete'), edit_delete_start_crypto)],
        states={
            "1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), edit_delete_choose_crypto
                )
            ],
            '2': [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), delete_price_choose_crypto
                    )

            ],
            '3': [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), edit_choose_confirm_crypto
                )
            ],
            '4': [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), edit_price_crypto
                )
            ]
        },
        fallbacks=[
            MessageHandler(Filters.regex('^(Отмена)$'), operation_cancel),
            MessageHandler(Filters.regex('^(Назад)$'), back_to_menu),
        ]
    )

    price = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Текущий курс'), get_price)],
        states={
            "get_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), getting_pair_price
                ),
            ],
            "get_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), getting_another_pair_price
                ),
            ]
        },
        fallbacks=[
            MessageHandler(Filters.regex('^(Отмена)$'), operation_cancel),
            MessageHandler(Filters.regex('^(Назад)$'), back_to_menu),
        ]
    )

    orders = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Создать ордер'), set_order)],
        states={
            "set_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), choosing_pair
                )
            ],
            "set_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), choosing_order_type
                )
            ],
            "set_step_3": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), choosing_order_side
                )
            ],
            "set_step_4": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), checking_price
                )
            ],
            "set_step_5": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), prepearing_order
                )
            ],
            "set_step_6": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)')), making_order
                )
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex('(Назад)'), crypto_shares_comands),
            MessageHandler(Filters.regex('(Отмена)'), operation_cancel)
        ]
    )

    close_order = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Отменить ордер'), choosing_order_for_close)],
        states={
            "close_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), applying_closing
                )
            ],
            "close_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), closing_order
                )
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex('(Отмена)'), operation_cancel),
            MessageHandler(Filters.regex('(Назад)'), back_to_menu)
        ]
    )

    pair_trade_history = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('История торгов'), get_trade_history)],
        states={
            "history_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), prepearing_trade_history
                )
            ],
            "history_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), getting_another_pair_orders
                )
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex('(Отмена)'), operation_cancel),
            MessageHandler(Filters.regex('(Назад)'), back_to_menu)
            ]
    )

    crypto_assets = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Add'), add_crypto)],
        states={
            "add_crypto_step_1": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), choosing_pair_for_target
                )
            ],
            "add_crypto_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), checking_price_for_target
                )
            ],
            "add_crypto_step_3": [
                MessageHandler(
                    Filters.text & (~Filters.regex('^(Отмена|Назад)$')), aplying_target
                )
            ],
        },
        fallbacks=[
            MessageHandler(Filters.regex('(Назад)'), crypto_shares_comands),
            MessageHandler(Filters.regex('(Отмена)'), operation_cancel),
        ]
    )

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
