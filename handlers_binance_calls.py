from binance_utils import binance_client
from keyboards import cancel_keyboard


def get_balance(update, contet):
    """Возвращает баланс пользователя на Binance"""

    result = binance_client.get_balance(full=True)
    message = "Баланс:\n"
    for ticker, value in result.items():
        message += f"{ticker}: Свободно - {value.get('free', '0')}, Замороженно - {value.get('locked', '0')}\n"
    update.message.reply_text(message, reply_markup=cancel_keyboard())
