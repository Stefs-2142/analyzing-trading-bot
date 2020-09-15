from binance_utils import binance_client
from keyboards import cancel_keyboard

from telegram.ext import ConversationHandler


def get_trade_history(update, context):
    """Получаем историю торгов по заданному тикеру."""

    update.message.reply_text(
        'Пришлите пару тикеров в формате "ETC USDT"',
        keyboard_markup=cancel_keyboard()
        )
    return 'history_step_1'


def prepearing_trade_history(update, context):  # history_step_1
    """
    Проверям валидность введёной пары тикеров для ордера
    """

    # Формируем пару тикеров из пользовательского ввода.
    ticker_pair = update.message.text.upper().split(' ')

    # Провереяем что пользователь ввёл 2 тикера.
    if len(ticker_pair) != 2:
        update.message.reply_text(
            'К сожалению, введена неверная пара, попробуйте ещё раз'
            ' или нажмите "Отмена" для завершения операции.',
            reply_markup=cancel_keyboard()
        )
        return "history_step_1"

    trade_history = binance_client.get_trade_history(
        ticker_pair[0], ticker_pair[1], is_time_stamp=False
        )
    update.message.reply_text(
        trade_history, keyboard_markup=cancel_keyboard()
        )
    return ConversationHandler.END


def __formated_message(update, context, trade_history):
    """Формируем сообщение из полученного списка 'trade_history'"""

    pass
