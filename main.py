import logging
import telegram


from handlers_binance_calls import binance_comands, get_balance, get_price
from handlers_binance_calls import get_step_1, get_step_2
from handler_binance_set_oreder import set_order, set_step_1
from handler_binance_set_oreder import set_step_2, set_step_3

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

from settings import TELEGRAM_API_KEY
from tasks import polling
from telegram.ext import (
    Updater, CommandHandler,
    MessageHandler, Filters, ConversationHandler
)

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    bot = telegram.Bot(TELEGRAM_API_KEY)

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
                    Filters.text & (~Filters.regex('(Отмена)')), get_step_1
                )
            ],
            "get_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), get_step_2
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
                    Filters.text & (~Filters.regex('(Отмена)')), set_step_1
                )
            ],
            "set_step_2": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), set_step_2
                )
            ],
            "set_step_3": [
                MessageHandler(
                    Filters.text & (~Filters.regex('(Отмена)')), set_step_3
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

    dp.add_handler(assets)
    dp.add_handler(edit_asssets)
    dp.add_handler(price)
    dp.add_handler(orders)

    dp.add_handler(MessageHandler(Filters.text, unknown_text))

    logging.info("Bot started")
    atb_bot.start_polling()
    polling.delay()

    atb_bot.idle()


if __name__ == "__main__":
    main()
