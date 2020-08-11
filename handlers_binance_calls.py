from binance_utils import BinanceClient
from keyboards import cancel_keyboard, main_binance_keyboard
from keyboards import another_pair_keyboard


binance_client = BinanceClient()


def binance_comands(update, context):
    """
    Функция, представляет доступные
    команды для работы с Binance
    """
    reply = 'Доступные команды.'
    update.message.reply_text(reply, reply_markup=main_binance_keyboard())


def get_balance(update, contet):
    """Возвращает баланс пользователя на Binance"""

    result = binance_client.get_balance()
    result_str = 'Ваш баланс:\n\n'
    for k, v in result.items():
        result_str += k
        result_str += ' - '
        result_str += v
        result_str += '\n'

    update.message.reply_text(result_str)


def get_price(update, context):
    """Зпрашиаем у пользователя пару тикеров для получения актуальной цены."""

    update.message.reply_text(
        'Введите пару тикеров в формате ETC USDT',
        reply_markup=cancel_keyboard()
    )

    return 'ticker'


def get_step_1(update, context):
    """Проверяем валидность введённых данных и зацикливаем если не валидно."""

    ticker_pair = update.message.text.upper().split(' ')

    # Провереяем что пользователь ввёл 2 тикера.
    if len(ticker_pair) != 2:
        update.message.reply_text(
            'К сожалению, введена неверная пара, попробуйте ещё раз'
            ' или нажмите "Отмена" для завершения операции.'
            )
        return 'ticker'
    result = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
            )
    if result is not None:
        update.message.reply_text(result, reply_markup=another_pair_keyboard())
        return 'step_2'
    update.message.reply_text(
        'К сожалению, введена неверная пара, попробуйте ещё раз.'
        )
    return 'ticker'


def get_step_2(update, context):
    """На этом шаге позволяем пользователю выбрать другой тикер."""

    if update.message.text != 'Другая пара':
        update.message.reply_text(
            'Пожалуйста, выберите одну из доступных команд.',
            reply_markup=another_pair_keyboard()
        )
        return 'step_2'

    update.message.reply_text(
        'Введите пару тикеров в формате ETC USDT',
        reply_markup=cancel_keyboard()
    )
    return 'ticker'
