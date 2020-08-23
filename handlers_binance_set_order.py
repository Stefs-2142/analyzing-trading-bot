from keyboards import cancel_keyboard, order_type_keyboard, quantity_keyboard
from keyboards import buy_sell_keyboard, aply_order_keyboard
from keyboards import KEYBOARD_PERCENT_POOL, ORDERS_TYPE, ORDERS_SIDE
from handlers_binance_calls import binance_client
from telegram.ext import ConversationHandler

from handlers_utils import clear_all_crypto


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


def choosing_pair(update, context):  # set_step_1
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


def choosing_order_type(update, context):  # set_step_2
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
    context.user_data['order_type'] = update.message.text.split()[0].lower()

    # Забираем ранее сохранённый список пары тикеров.
    ticker_pair = context.user_data['ticker_pair']

    # Сохраняем баланс пользователя.
    balance = binance_client.get_balance()
    context.user_data['balance'] = balance

    # Создаём 2 строчки и записываем достуный баланс выбранных пар.
    ticker_1 = balance.get(ticker_pair[1], '0') + " " + ticker_pair[1]
    ticker_2 = balance.get(ticker_pair[0], '0') + " " + ticker_pair[0]

    update.message.reply_text(
        "Выберите сторону сделки.", reply_markup=buy_sell_keyboard(ticker_1, ticker_2)
    )

    return "set_step_3"


def choosing_order_side(update, context):  # set_step_3
    """
    Проверяем выбранную сторону сделки.
    Доступны 'Купить', 'Продать'.
    """

    # Забираем ранее сохранённый список пары тикеров.
    balance = binance_client.get_balance()
    ticker_pair = context.user_data['ticker_pair']

    # Создаём 2 строчки и записываем достуный баланс выбранных пар.
    ticker_1 = balance.get(ticker_pair[1], '0') + " " + ticker_pair[1]
    ticker_2 = balance.get(ticker_pair[0], '0') + " " + ticker_pair[0]

    if update.message.text not in ORDERS_SIDE:
        update.message.reply_text(
                'Пожалуйста, выберите сторону сделки или нажмите "Отмена".',
                reply_markup=buy_sell_keyboard(ticker_1, ticker_2)
                )
        return 'set_step_3'

    # Cохраняем сторону сделки.
    context.user_data['order_side'] = update.message.text

    if context.user_data['order_type'] == 'limit':

        update.message.reply_text(
            'Введите цену.', reply_markup=cancel_keyboard()
        )
        return 'set_step_4'

    allowed_balance = ''
    if context.user_data['order_side'] == 'sell':
        allowed_balance += ticker_2
    else:
        allowed_balance += ticker_1

    update.message.reply_text(
        f'Выберите количество.\n Доступно - {allowed_balance}',
        reply_markup=quantity_keyboard()

    )

    return 'set_step_5'


def checking_price(update, context):  # set_step_4

    """ TODO Нужно добоавить расчёт максимальной и минимальной глубины ордера для каждой пары.
    Если пропустить тут цену в 1$ для BTC упадём с ошибкой по API.
    """

    try:
        price = abs(float(update.message.text))
    except (ValueError, TypeError):
        update.message.reply_text(
            'Пожалуйста, введите корректную цену.',
            reply_markup=cancel_keyboard()
        )
        return 'set_step_4'
    else:
        # Сохраняем цену.
        context.user_data['price'] = price
        update.message.reply_text(
            'Выберите количество.', reply_markup=quantity_keyboard()
        )
        return 'set_step_5'


def prepearing_order(update, context):  # set_step_5

    if update.message.text not in KEYBOARD_PERCENT_POOL:
        update.message.reply_text(
            'Выберите количество.', reply_markup=quantity_keyboard()
        )
        return 'set_step_5'

    percent = int(update.message.text.replace('%', '')) / 100

    # Забираем ранее сохранённый список пары тикеров.
    ticker_pair = context.user_data['ticker_pair']

    # Забираем ранее сохранёную сторону сделки.
    order_side = context.user_data['order_side']

    # Забираем ранене сохранённый баланс.
    balance = context.user_data['balance']

    # Забираем ранее сохранённый тип сделки.
    order_type = context.user_data['order_type']

    # Забираем ранее сохранённую цену.
    price = context.user_data.get('price', None)

    # Делаем повторный запрос для актуализиции данных.
    result = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
        )

    def __prepearing_message(
        context=context, update=update,
        ticker_pair=ticker_pair, order_side=order_side,
        balance=balance, order_type=order_type,
        price=price, result=result
    ):
        """Формируем сообщение."""

        if order_side == 'buy':
            formated_quantity = percent * float(balance[ticker_pair[1]])

            # Cохраняем выбранное количество для сделки.
            context.user_data['quantity'] = formated_quantity

            if order_type == 'market':
                message = f"Купить {formated_quantity} {ticker_pair[1]} по текущему курсу {result} ?"
                return message
            elif order_type == 'limit':
                message = f"Выставить ордер на покупку {formated_quantity} {ticker_pair[1]} по курсу {price} {ticker_pair[0]} ?"
                return message
        else:
            formated_quantity = percent * float(balance[ticker_pair[0]])

            # Cохраняем выбранное количество для сделки.
            context.user_data['quantity'] = formated_quantity

            if order_type == 'market':
                message = f"Продать {formated_quantity} {ticker_pair[0]} по текущему курсу {result} ?"
                return message
            elif order_type == 'limit':
                message = f"Выставить ордер на продажу {formated_quantity} {ticker_pair[0]} по курсу {price} {ticker_pair[1]} ?"
                return message

    message = __prepearing_message()

    update.message.reply_text(
        message, reply_markup=aply_order_keyboard(order_side)
        )

    return 'set_step_6'


def making_order(update, context):  # set_step_6

    if update.message.text not in ORDERS_SIDE:
        update.message.reply_text(
            'Подвтердите сделку или нажмите "Отмена"',
            reply_markup=aply_order_keyboard(
                context.user_data['order_side']
            )
        )
        return 'set_step_6'

    # Забираем ранее сохранённый список пары тикеров.
    ticker_pair = context.user_data['ticker_pair']

    # Забираем ранее сохранёную сторону сделки.
    order_side = context.user_data['order_side']

    # Забираем ранее сохранённый тип ордера.
    order_type = context.user_data['order_type']

    # Забираем ранее сохранённое количество для сделки.
    quantity = int(context.user_data['quantity'])

    # Забирем цену, оставляем пустой если Marker order.
    price = context.user_data.get('price', None)

    # Формируем сделку.
    result = binance_client.set_order(
            ticker_pair[0], ticker_pair[1],
            order_type, order_side, quantity, price
        )
    if result is not None:
        update.message.reply_text('Ордер выставлен!')

        clear_all_crypto(update, context)

        return ConversationHandler.END

    update.message.reply_text(
        'Возникла ошибка.',
        reply_markup=cancel_keyboard()
    )
    clear_all_crypto(update, context)