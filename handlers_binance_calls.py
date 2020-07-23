from binance_utils import BinanceClient
from keyboards import main_shares_keyboard, main_menu_keyboard, main_binance_keyboard


binance_client = BinanceClient()


def binance_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с Binance
    """
    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_binance_keyboard())


def get_price(update, context):
    """Зпрашиаем у пользователя пару тикеров для получения актуальной цены."""

    if context.args:
        user_text = context.args
        try:
            result = binance_client.average_price(user_text[0], user_text[1])
            update.message.reply_text(result)
        except (TypeError, ValueError):
            message = 'Ведите пару ещё раз'
            update.message.reply_text(message)


def get_balance(update, contet):
    """Возвращает баланс пользователя на Binance"""

    result = binance_client.get_balance()
    update.message.reply_text(result)
