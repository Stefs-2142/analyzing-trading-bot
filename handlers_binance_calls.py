from binance_utils import BinanceClient


def get_balance(update, context):
    """Зпрашиаем у пользователя пару тикеров для получения актуальной цены."""

    update.message.reply_text(
        'Введите пару тикеров в формате ETC/USDT'
    
    )
    if context.args:
        user_text = context.args.split(' ')
        try:
            result = BinanceClient().average_price(user_text[0], user_text[1])
            update.message.reply_text(result)
        except (TypeError, ValueError):
            message = 'Ведите пару ещё раз'
            update.message.reply_text(message)