from telegram.ext import ConversationHandler

from keyboards import (aply_order_keyboard, buy_sell_keyboard,
                       cancel_keyboard, quantity_keyboard,
                       main_menu_keyboard, order_type_keyboard)

from keyboards import KEYBOARD_PERCENT_POOL
from keyboards import ORDERS_TYPE
from keyboards import ORDERS_SIDE

from binance_utils import binance_client

from .utils import clear_all_crypto, autorization


@autorization
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


# set_step_1
def choosing_pair(update, context):
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
        return "set_step_1"

    # Сохраняем введёную пару тикеров.
    context.user_data['order_info'] = {}
    context.user_data['order_info']['ticker_pair'] = ticker_pair

    # Узнаём текущий курс.
    current_price = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
        )

    if current_price is not None:
        update.message.reply_text(
            f'Текущая цена заданной пары {current_price}\n'
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


# set_step_2
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
    context.user_data['order_info']['order_type'] = update.message.text.split()[0].lower()

    context.user_data['order_info']['price'] = None

    # Забираем ранее сохранённый список пары тикеров.
    ticker_pair = context.user_data['order_info']['ticker_pair']

    # Сохраняем баланс пользователя.
    balance = binance_client.get_balance(full=False)
    context.user_data['order_info']['balance'] = balance

    # Создаём 2 строчки и записываем достуный баланс выбранных пар.
    ticker_1_balance = balance.get(ticker_pair[1], '0') + " " + ticker_pair[1]
    ticker_2_balance = balance.get(ticker_pair[0], '0') + " " + ticker_pair[0]

    context.user_data['order_info']['ticker_1_balance'] = ticker_1_balance
    context.user_data['order_info']['ticker_2_balance'] = ticker_2_balance

    update.message.reply_text(
        "Выберите сторону сделки.",
        reply_markup=buy_sell_keyboard(ticker_1_balance, ticker_2_balance)
    )
    return "set_step_3"


# set_step_3
def choosing_order_side(update, context):
    """
    Проверяем выбранную сторону сделки.
    Доступны 'Купить', 'Продать'.
    """

    # Забираем ранее сохранённые балансы пар.
    ticker_1_balance = context.user_data['order_info']['ticker_1_balance']
    ticker_2_balance = context.user_data['order_info']['ticker_2_balance']

    if update.message.text not in ORDERS_SIDE:
        update.message.reply_text(
                'Пожалуйста, выберите сторону сделки или нажмите "Отмена".',
                reply_markup=buy_sell_keyboard(ticker_1_balance, ticker_2_balance)
                )
        return 'set_step_3'

    context.user_data['order_info'].pop('ticker_1_balance')
    context.user_data['order_info'].pop('ticker_2_balance')

    # Cохраняем сторону сделки.
    context.user_data['order_info']['order_side'] = update.message.text
    # Возвращаем в начало шага если баланс выбранного тикера равен 0.
    allowed_balance = ''
    if context.user_data['order_info']['order_side'] == 'sell':
        if float(ticker_2_balance.split()[0]) == 0:
            update.message.reply_text(
                'Недостаточно средств.', keyboard_markup=main_menu_keyboard()
                )
            return 'set_step_3'
        allowed_balance += ticker_2_balance
    else:
        if float(ticker_1_balance.split()[0]) == 0:
            update.message.reply_text(
                'Недостаточно средств.', keyboard_markup=main_menu_keyboard()
                )
            return 'set_step_3'
        allowed_balance += ticker_1_balance

    if context.user_data['order_info']['order_type'] == 'limit':
        update.message.reply_text(
            'Введите цену.', reply_markup=cancel_keyboard()
        )
        return 'set_step_4'

    update.message.reply_text(
        f'Выберите количество.\n Доступно - {allowed_balance}',
        reply_markup=quantity_keyboard()
    )
    return 'set_step_5'


# set_step_4
def checking_price(update, context):

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
        context.user_data['order_info']['price'] = price
        update.message.reply_text(
            'Выберите количество.', reply_markup=quantity_keyboard()
        )
        return 'set_step_5'


# set_step_5
def prepearing_order(update, context):
    """Собираем все данные для сделки."""

    if update.message.text not in KEYBOARD_PERCENT_POOL:
        update.message.reply_text(
            'Выберите количество.', reply_markup=quantity_keyboard()
        )
        return 'set_step_5'

    percentage = int(update.message.text.replace('%', '')) / 100

    (ticker_pair, order_type, price, balance, order_side) = context.user_data['order_info'].values()

    # Делаем повторный запрос для актуализиции данных.
    actual_price = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
        )

    def __prepearing_quantity(quantity):
        """
        Расчитывем разрешённое количество для сделки,
        загружая данные по заданной паре тикеров.
        Ecли пользователь хочет купить/продать 0.5215215365434 ETC
        Проданно/куплено будет 0.52, так как stepSize для ETC = 0.01
        """

        # Получаем торговые свойства пары.
        symbol_info = binance_client.get_symbol_info(ticker_pair[0]+ticker_pair[1])

        for filters in symbol_info['filters']:
            if filters['filterType'] == 'LOT_SIZE':
                symbol_step_size = filters.get('stepSize')

        # Cчитаем количество знаков после точки.
        len_num = len(symbol_step_size.rstrip('0').split('.')[1])
        # Отсекаем лишнее.
        prepared_quantity = int(quantity * 10 ** len_num) / 10 ** len_num
        return prepared_quantity

    def __prepearing_message(
        context=context, update=update,
        ticker_pair=ticker_pair, order_side=order_side,
        balance=balance, order_type=order_type,
        price=price, actual_price=actual_price
    ):
        """
        Формируем итоговое сообщение в котором
        содержится вся информация по сделке.
        """
        if order_side == 'buy':
            allowed_quantity = ((float(balance[ticker_pair[1]]) * percentage) / float(actual_price.split()[0]))
            formated_quantity = __prepearing_quantity(allowed_quantity)

            # Cохраняем выбранное количество для сделки.
            context.user_data['order_info']['quantity'] = formated_quantity

            if order_type == 'market':
                message = f"Купить {formated_quantity} {ticker_pair[0]} по текущему курсу {actual_price} ?"
                return message
            elif order_type == 'limit':
                message = f"Выставить ордер на покупку {formated_quantity} {ticker_pair[0]} по курсу {price} {ticker_pair[1]} ?"
                return message

        # order_side = 'sell'
        else:
            allowed_quantity = percentage * float(balance[ticker_pair[0]])
            formated_quantity = __prepearing_quantity(allowed_quantity)

            # Cохраняем выбранное количество для сделки.
            context.user_data['order_info']['quantity'] = formated_quantity

            if order_type == 'market':
                message = f"Продать {formated_quantity} {ticker_pair[0]} по текущему курсу {actual_price} ?"
                return message
            elif order_type == 'limit':
                message = f"Выставить ордер на продажу {formated_quantity} {ticker_pair[0]} по курсу {price} {ticker_pair[1]} ?"
                return message

    message = __prepearing_message()

    update.message.reply_text(
        message, reply_markup=aply_order_keyboard(order_side)
        )
    return 'set_step_6'


# set_step_6
def making_order(update, context):

    if update.message.text not in ORDERS_SIDE:
        update.message.reply_text(
            'Подвтердите сделку или нажмите "Отмена"',
            reply_markup=aply_order_keyboard(
                context.user_data['order_info']['order_side']
            )
        )
        return 'set_step_6'

    (ticker_pair, order_type, price, balance, order_side, quantity) = context.user_data['order_info'].values()

    # Минимально допустимая сумма сделки в $
    min_order_summ_in_usdt = 10

    def __preaparing_order_summ(price=price):
        """
        Если ордер создаётся для пары без $
        Например BNB/BTC - расчитываем price в $
        """
        if ticker_pair[1] != 'USDT' and order_type == 'limit':
            summ_in_usdt = binance_client.get_average_price(
                ticker_pair[0], 'USDT'
            )
            price *= float(summ_in_usdt.split()[0])

        elif ticker_pair[1] != 'USDT' and order_type == 'market':
            result_usdt = binance_client.get_average_price(
                ticker_pair[0], 'USDT'
            )
            price = float(result_usdt.split()[0])

        elif order_type == 'market':
            result_usdt = binance_client.get_average_price(
                ticker_pair[0], 'USDT'
            )
            price = float(result_usdt.split()[0])

        current_order_summ = price*quantity
        return current_order_summ

    # Сумма ордера.
    current_order_summ = __preaparing_order_summ()

    # Проверяем сумму ордера и если она меньше 10$ отправляем обратно.
    if current_order_summ < min_order_summ_in_usdt:
        message = f'Ордер должен быть не меньше {min_order_summ_in_usdt}$'
        message += f'\nВаш - {current_order_summ}$'
        update.message.reply_text(
            message,
            reply_markup=cancel_keyboard()
            )
        return 'set_step_4'

    if order_type == 'market' and order_side == 'sell':
        result = binance_client.set_order_market_sell(
            ticker_pair[0], ticker_pair[1],
            quantity
        )
    elif order_type == 'market' and order_side == 'buy':
        result = binance_client.set_order_market_buy(
            ticker_pair[0], ticker_pair[1],
            quantity
        )
    # Формируем и совершаем сделку.
    elif order_type == 'limit':
        result = binance_client.set_order(
                ticker_pair[0], ticker_pair[1],
                order_type, order_side, quantity, price
            )
    if result is not None:
        update.message.reply_text(
            'Ордер выставлен!', reply_markup=main_menu_keyboard()
        )

        clear_all_crypto(update, context)
        return ConversationHandler.END

    update.message.reply_text(
        'Возникла ошибка.',
        reply_markup=cancel_keyboard()
    )
    clear_all_crypto(update, context)
    return ConversationHandler.END
