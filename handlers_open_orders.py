from binance_utils import binance_client


def get_open_orers(update, context):
    """Получаем список отрктых ордеров на бирже."""

    open_orders = binance_client.get_all_open_orders()

    update.message.reply_text(open_orders)
