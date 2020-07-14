import telegram


from celery import Celery
from models import Asset
from settings import API_KEY, BACKEND_PATH, BROKER_PATH
from ticker_utils import ticker_pricing
from time import sleep


app = Celery('tasks', backend=BACKEND_PATH, broker=BROKER_PATH)


@app.task
def polling():
    bot = telegram.Bot(API_KEY)
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
    while True:
        alerted_tickers = ticker_pricing(Asset().get_polling_data())
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
        else:
            pass
        sleep(60)
