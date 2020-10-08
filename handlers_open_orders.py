from binance_utils import binance_client
from keyboards import back_keyboard


def get_open_orers(update, context):
    """Получаем список отрктых ордеров на бирже."""

    open_orders = binance_client.get_all_open_orders()
    # Если получаем пустой список - отрытых ордеров нет.
    if open_orders:
        formated_orders = ""
        for i, order in enumerate(open_orders, start=1):
            formated_orders += f"{i}. {order['symbol']}"
            formated_orders += f" {order['type']} {order['side']}"
            formated_orders += f" {order['price']}\n"

        update.message.reply_text(
            f"{formated_orders}\n", reply_markup=back_keyboard()
            )
    else:
        update.message.reply_text(
            'Нет открытых ордеров.', keyboard_markup=back_keyboard()
            )
