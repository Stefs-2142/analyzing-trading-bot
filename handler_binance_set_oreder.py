from setting import ORDERS_TYPE
from keyboards import cancel_keyboard, order_type_keyboard
from handlers_binance_calls import binance_client
from telegram.ext import ConversationHandler


def set_order(update, contet):
    """
    Функция с которой начинается диалог для
    выставления ордера на бирже.
    """

    update.message.reply_text(
        'Какой тип ордер необходио выставить?',
        reply_markup=order_type_keyboard()
    )

    return 'set_step_1'


def set_step_1(update, context):
    """Проверяем выбрал ли пользователь доступный тип ордера."""

    if update.message.text not in ORDERS_TYPE:
        update.message.reply_text(
            'Пожалуйста, выберите одну из доступных команд',
            reply_markup=order_type_keyboard()
            )
        return 'set_step_1'
    context.user_data['order_type'] = update.message.text
    update.message.reply_text(context.user_data)
    return 'set_step_2'


def set_step_2(update, context):
    """Спрашиваем для какой пары необходимо выставить ордер."""

    update.message.reply_text(
        'Пришлите пару для ордера в формате BTC USDT',
        reply_markup=cancel_keyboard()
        )
    ticker_pair = update.message.text.upper().split(' ')

    # Провереяем что пользователь ввёл 2 тикера.
    if len(ticker_pair) != 2:
        update.message.reply_text(
            'К сожалению, введена неверная пара, попробуйте ещё раз'
            ' или нажмите "Отмена" для завершения операции.',
            reply_markup=cancel_keyboard()
            )
        return 'set_step_2'
    result = binance_client.get_average_price(
        ticker_pair[0], ticker_pair[1]
            )
    if result is not None:
        update.message.reply_text(
            f'Текущая цена заданной пары -{result}',
            reply_markup=cancel_keyboard()
            )
        return 'set_step_3'

    update.message.reply_text(
        'К сожалению, введена неверная пара, попробуйте ещё раз.'
        )
    return 'set_step_2'


def set_step_3(update, context):

    # TODO: Добавить следующие шаги для совершения ордера.
    return ConversationHandler.END
