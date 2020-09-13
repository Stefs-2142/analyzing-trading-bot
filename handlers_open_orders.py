from binance_utils import binance_client
from keyboards import main_menu_keyboard


def get_open_orers(update, context):
    """Получаем список отрктых ордеров на бирже."""

    open_orders = binance_client.get_all_open_orders()
    # Если получаем пустой список - отрытых ордеров нет.
    if open_orders:
        formated_orders = ""
        order_count = 1
        for order in open_orders:
            formated_orders += f"{order_count}. {order['symbol']}"
            formated_orders += f" {order['type']} {order['side']}"
            formated_orders += f" {order['price']}\n"
            order_count += 1

        update.message.reply_text(
            f"{formated_orders}\n", reply_markup=main_menu_keyboard()
            )
    else:
        update.message.reply_text(
            'Нет открытых ордеров.', keyboard_markup=main_menu_keyboard()
            )
