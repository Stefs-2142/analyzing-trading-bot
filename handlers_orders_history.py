from binance_utils import binance_client
from keyboards import back_keyboard, another_pair_back_keyboard


def get_trade_history(update, context):
    """Получаем историю торгов по заданному тикеру."""

    update.message.reply_text(
        'Пришлите пару тикеров в формате "ETC USDT"',
        reply_markup=back_keyboard()
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
            reply_markup=back_keyboard()
        )
        return "history_step_1"

    update.message.reply_text(
        'Проверяю, пару, загружаю данные...', reply_markup=back_keyboard()
        )
    trade_history = binance_client.get_trade_history(
        ticker_pair[0], ticker_pair[1], is_time_stamp=False
        )
    # Проверяем существует ли история по введённой паре.
    if trade_history:
        formated_message = __form_a_message(trade_history)
        update.message.reply_text(
            formated_message, reply_markup=another_pair_back_keyboard()
            )
        return 'history_step_2'
    else:
        update.message.reply_text(
            'Нет истории по заданной паре. Попробуйте ещё раз.',
            reply_markup=back_keyboard()
            )
        return 'history_step_1'


def getting_another_pair_orders(update, context):  # history_step_2
    """На этом шаге позволяем пользователю выбрать другую пару."""

    if update.message.text != 'Другая пара':
        update.message.reply_text(
            'Пожалуйста, выберите одну из доступных команд.',
            reply_markup=another_pair_back_keyboard()
        )
        return "history_step_2"

    update.message.reply_text(
        'Введите пару тикеров в формате ETC USDT',
        reply_markup=back_keyboard()
    )
    return "history_step_1"


def __form_a_message(trade_history):
    """
    Формируем сообщение из полученного списка 'trade_history'
    Отбрасываем лишние нули
    """
    message = 'Дата || Пара || Сторона || Цена || Количество || Сумма\n\n\n'
    for trade in trade_history:
        message += f"{trade['time']}| "
        message += f"{trade['symbol']}| "
        message += f"{trade['order_side']}| "
        message += f"{float(trade['price'])}| "
        message += f"{float(trade['quantity'])}| "
        message += f"{float(trade['quoteQty'])}\n\n\n"
    return message
