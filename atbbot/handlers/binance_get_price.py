from keyboards import another_pair_back_keyboard, back_keyboard

from binance_utils import binance_client


def get_price(update, context):
    """Зпрашиаем у пользователя пару тикеров для получения актуальной цены."""

    update.message.reply_text(
        'Введите пару тикеров в формате ETC USDT',
        reply_markup=back_keyboard()
    )

    return "get_step_1"


def getting_pair_price(update, context):
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
        update.message.reply_text(result, reply_markup=another_pair_back_keyboard())
        return "get_step_2"

    update.message.reply_text(
        'К сожалению, введена неверная пара, попробуйте ещё раз.',
        reply_markup=back_keyboard()
        )
    return 'ticker'


def getting_another_pair_price(update, context):
    """На этом шаге позволяем пользователю выбрать другой тикер."""

    if update.message.text != 'Другая пара':
        update.message.reply_text(
            'Пожалуйста, выберите одну из доступных команд.',
            reply_markup=another_pair_back_keyboard()
        )
        return 'step_2'

    update.message.reply_text(
        'Введите пару тикеров в формате ETC USDT',
        reply_markup=another_pair_back_keyboard()
    )
    return 'ticker'
