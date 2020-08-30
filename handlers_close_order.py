from binance_utils import binance_client
from keyboards import numbers_keyboard, yes_no_keyboard
from keyboards import main_menu_keyboard
from keyboards import NUMBERS
from telegram.ext import ConversationHandler


def choosing_order_for_close(update, context):
    """Спрашиваем у пользователя какой ордер закрыть."""

    open_orders = binance_client.get_all_open_orders()
    
    # Сохраняем открытые ордера.
    context.user_data['open_orders'] = open_orders

    formated_orders = ""
    order_count = 1
    for order in open_orders:
        formated_orders += f"{order_count}. {order['symbol']}"
        formated_orders += f" {order['type']} {order['side']}"
        formated_orders += f" {order['price']}\n"
        order_count += 1

    update.message.reply_text(
        f"{formated_orders}\nВыберите ордер для закрытия.",
        reply_markup=numbers_keyboard()
        )
    return 'close_step_1'


def applying_closing(update, context):
    """Подтверждаем закрытие оредра."""

    if update.message.text not in NUMBERS:
        update.message.reply_text(
            'Пожалуйста, выберите, ордер для закрытия или нажмите "Отмена"'
        )
        return 'close_step_1'

    # Сохраняем в выбранный ордер для закрытия.
    context.user_data['order_count_for_close'] = int(update.message.text)

    update.message.reply_text(
        'Отменить ордер?', reply_markup=yes_no_keyboard()
    )
    return 'close_step_2'


def closing(update, context):
    """Закрываем ордер."""

    if update.message.text != 'Да':
        update.message.reply_text(
            'Что дальше?', reply_markup=main_menu_keyboard()
        )
        return ConversationHandler.END

    # Cохраняем выбранный ордер для закрытия.
    order_count_for_close = context.user_data['order_count_for_close']
    # Забираем пару тикеров для закрытия ордера в формате 'ETCUSDT'.
    symbol = context.user_data['open_orders'][order_count_for_close - 1].get('symbol')
    # Забираем 'orderId' ордера для его закрытия.
    orderId = context.user_data['open_orders'][order_count_for_close - 1].get('orderId')

    try:
        binance_client.close_order(symbol, orderId)
    # Блок 'except' неявный намеренно - ошибки отлавливаются уровнем ниже.
    except:
        update.message.reply_text(
            'Упс! Возникла ошибка.', reply_markup=main_menu_keyboard()
        )
    else:
        update.message.reply_text(
            "Ордер закрыт!", reply_markup=main_menu_keyboard()
        )
        return ConversationHandler.END
