from settings import ORDERS_TYPE, ORDERS_SYDE, PERCENT_POOL
from keyboards import cancel_keyboard, order_type_keyboard, quantity_keyboard
from keyboards import buy_sell_keyboard, aply_order_keyboard
from handlers_binance_calls import binance_client
from telegram.ext import ConversationHandler


def set_order(update, context):
    """
    Функция с которой начинается диалог для
    выставления ордера на бирже.
    """

    update.message.reply_text(
        'Пришлите пару для ордера в формате BTC USDT',
        reply_markup=cancel_keyboard()
        )
    return "set_step_1"


def choosing_pair(update, context):
    """
    Проверям валидность введёной пары тикеров для ордера
    """

    # Формируем пару тикеров из прошлого пользовательского ввода.
    ticker_pair = update.message.text.upper().split(' ')

    # Сохраняем введёную пару тикеров.
    context.user_data['ticker_pair'] = ticker_pair

    # Провереяем что пользователь ввёл 2 тикера.
    if len(ticker_pair) != 2:
        update.message.reply_text(
            'К сожалению, введена неверная пара, попробуйте ещё раз'
            ' или нажмите "Отмена" для завершения операции.',
            reply_markup=cancel_keyboard()
        )
        return "set_step_1"

    # Делаем запрос к API и узнаём текущий курс.
    result = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
        )

    if result is not None:
        update.message.reply_text(
            f'Текущая цена заданной пары {result}\n'
            'Пожалуйста, выберите тип ордера или нажмите "Отмена".',
            reply_markup=order_type_keyboard()
        )
        return "set_step_2"

    # Возвращаем на шаг назад если пара тикеров невалидна.
    update.message.reply_text(
        'К сожалению, введена неверная пара, попробуйте ещё раз.',
        reply_markup=cancel_keyboard()
        )
    return "set_step_1"


def choosing_order_type(update, context):
    """
    Проверяем выбрал ли пользователь доступный тип ордера,
    Сейчас доступны: Limit order и Market order
    """

    if update.message.text not in ORDERS_TYPE:
        update.message.reply_text(
            'Пожалуйста, выберите тип ордера или нажмите "Отмена".',
            reply_markup=order_type_keyboard()
            )
        return "set_step_2"

    # Cохраняем выбранный пользователем тип ордера.
    context.user_data['order_type'] = update.message.text

    # Забираем ранее сохранённый список пары тикеров.
    ticker_pair = context.user_data['ticker_pair']

    # Сохраняем баланс пользователя.
    balance = binance_client.get_balance()
    context.user_data['balance'] = balance

    # Создаём 2 строчки и записываем достуный баланс выбранных пар.
    ticker_1 = balance.get(ticker_pair[1], '0') + " " + ticker_pair[1]
    ticker_2 = balance.get(ticker_pair[0], '0') + " " + ticker_pair[0]

    ticker_pair = context.user_data['ticker_pair']

    update.message.reply_text(
        "Выберите сторону сделки.", reply_markup=buy_sell_keyboard(ticker_1, ticker_2)
    )

    return "set_step_3"


def choosing_order_side(update, context):
    """
    Проверяем выбранную сторону сделки.
    Доступны 'Купить', 'Продать'.
    """

    if update.message.text not in ORDERS_SYDE:
        update.message.reply_text(
                'Пожалуйста, выберите сторону сделки или нажмите "Отмена".'
                )
        return 'set_step_3'

    # Cохраняем сторону сделки.
    context.user_data['order_side'] = update.message.text

    update.message.reply_text(
        'Выберите количество.', reply_markup=quantity_keyboard()
    )
    return 'set_step_4'


def making_order(update, context):

    if update.message.text not in PERCENT_POOL:
        update.message.reply_text(
            'Выберите количество.', reply_markup=quantity_keyboard()
        )
        return 'set_step_3'

    percent = int(update.message.text.replace('%', '')) / 100

    # Забираем ранее сохранённый список пары тикеров.
    ticker_pair = context.user_data['ticker_pair']

    # Забираем ранее сохранёную сторону сделки.
    order_side = context.user_data['order_side']

    # Забираем ранене сохранённый баланс.
    balance = context.user_data['balance']

    # Делаем повторный запрос для актуализиции данных.
    result = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
        )

    if order_side == 'Купить':
        formated_balance = percent * float(balance[ticker_pair[1]])
        message = f'Купить {ticker_pair[0]} по текущему курсу '
        message += f'{result} на сумму {formated_balance})?'
    else:
        formated_balance = percent * float(balance[ticker_pair[0]])
        message = f'Продать {ticker_pair[0]} по текущему курсу '
        message += f'{result} на сумму {formated_balance}?'

    update.message.reply_text(
        message, reply_markup=aply_order_keyboard()
        )

    return 'set_step_5'


def order_status(update, context):

    update.message.reply_text('cool all ok!')

    return ConversationHandler.END
