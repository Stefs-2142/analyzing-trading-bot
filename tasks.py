from settings import TELEGRAM_API_KEY

from celery_bot import app

import telegram

from models import Asset
from ticker_utils import ticker_pricing, ticker_crypto_pricing


bot = telegram.Bot(TELEGRAM_API_KEY)


@app.task
def beat_crypto_pooling():

    text_end = (
        'Отслеживание стоимости для инструмента прекращено, '
        'для установки новой стоимости для отслеживания - '
        'воспользуйтесь кнопкой "Изменить/Удалить"'
    )
    text_t_price = (
        'Достигнута максимальная цена для тикера %s. '
    )
    text_m_price = (
        'Достигнута минимальная цена для тикера %s. '
    )

    alerted_tickers = ticker_crypto_pricing(
        Asset().get_polling_data(is_crypto=True)
    )
    if alerted_tickers:
        for ticker in alerted_tickers:
            user_id, ticker_id, t_price, m_price = ticker
            if t_price is True:
                reply_message = (
                    (text_t_price % ticker_id) + text_end
                )
                Asset().edit_t_price(user_id, ticker_id, 0)
            else:
                reply_message = (
                    (text_m_price % ticker_id)+text_end
                )
                Asset().edit_m_price(user_id, ticker_id, 0)
        bot.send_message(user_id, reply_message)


@app.task
def beat_classic_pooling():

    text_end = (
        'Отслеживание стоимости для инструмента прекращено, '
        'для установки новой стоимости для отслеживания - '
        'воспользуйтесь кнопкой "Изменить/Удалить"'
    )
    text_t_price = (
        'Достигнута максимальная цена для тикера %s. '
    )
    text_m_price = (
        'Достигнута минимальная цена для тикера %s. '
    )

    alerted_tickers = ticker_pricing(
        Asset().get_polling_data(is_crypto=False)
    )
    if alerted_tickers:
        for ticker in alerted_tickers:
            user_id, ticker_id, t_price, m_price = ticker
            if t_price is True:
                reply_message = (
                    (text_t_price % ticker_id) + text_end
                )
                Asset().edit_t_price(user_id, ticker_id, 0)
            else:
                reply_message = (
                    (text_m_price % ticker_id)+text_end
                )
                Asset().edit_m_price(user_id, ticker_id, 0)
        bot.send_message(user_id, reply_message)
