from binance_utils import binance_client
from keyboards import cancel_keyboard


def get_balance(update, contet):
    """Возвращает баланс пользователя на Binance"""

    result = binance_client.get_balance()
    result_str = 'Ваш баланс:\n\n'
    for k, v in result.items():
        result_str += k
        result_str += ' - '
        result_str += v
        result_str += '\n'

    update.message.reply_text(result_str, reply_markup=cancel_keyboard())
