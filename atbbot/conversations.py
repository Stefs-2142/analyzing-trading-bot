from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from handlers.binance_set_order import (choosing_order_type, choosing_pair,
                                        choosing_order_side, checking_price,
                                        prepearing_order, set_order, making_order)

from handlers.binance_get_price import getting_another_pair_price
from handlers.binance_get_price import getting_pair_price
from handlers.binance_get_price import get_price

from handlers.close_order import applying_closing
from handlers.close_order import choosing_order_for_close
from handlers.close_order import closing_order

from handlers.orders_history import get_trade_history
from handlers.orders_history import getting_another_pair_orders
from handlers.orders_history import prepearing_trade_history

from handlers.crypto_asset_add import (add_crypto, aplying_target,
                                       choosing_pair_for_target, checking_price_for_target)

from handlers.asset_add import (add_start, add_step_1,
                                add_step_2, add_step_3, add_step_4)

from handlers.asset_edit_del import (delete_price_choose, edit_delete_choose,
                                     edit_delete_start, edit_choose_confirm, edit_price)

from handlers.crypto_asset_edit_del import (edit_delete_choose_crypto, edit_delete_start_crypto, 
                                            delete_price_choose_crypto, edit_choose_confirm_crypto,
                                            edit_price_crypto)

from handlers.utils import back_to_menu
from handlers.utils import crypto_shares_comands
from handlers.utils import operation_cancel


assets = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^Добавить'), add_start),],
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
    entry_points=[MessageHandler(Filters.regex('^Изменить/Удалить'), edit_delete_start)],
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
    entry_points=[MessageHandler(Filters.regex('^Edit/Delete'), edit_delete_start_crypto)],
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

crypto_assets = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^Add'), add_crypto)],
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

price = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^Текущий курс'), get_price)],
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
    entry_points=[MessageHandler(Filters.regex('^Создать ордер'), set_order)],
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
    entry_points=[MessageHandler(Filters.regex('^Отменить ордер'), choosing_order_for_close)],
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
    entry_points=[MessageHandler(Filters.regex('^История торгов'), get_trade_history)],
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
