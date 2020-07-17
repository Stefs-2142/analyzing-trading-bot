import telegram
import logging


from binance_utils import BinanceClient
from celery import Celery
from models import Asset
from settings import API_KEY, BACKEND_PATH, BROKER_PATH
from ticker_utils import ticker_pricing
from time import sleep


app = Celery('tasks', backend=BACKEND_PATH, broker=BROKER_PATH)


def make_celery():
    celery = Celery(
        backend='rpc://',
        broker='amqp://localhost'
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery_app = make_celery()
binance_client = BinanceClient()


@celery_app.on_after_configure.connect
def setup_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, set_alert.s())


@celery_app.task
def set_alert(ticket_1, ticket_2, target):
    "Каждые 10 секунд опрашивает цену заданного тикера на Binance"

    three_percent = 0.03
    sub_target_low = round((target - target * three_percent), 1)  # Зададём границы таргета в 3%
    sub_target_hight = round((target + target * three_percent), 1)
    logging.info('Таргет установлен.')

    while True:
        sleep(10)
        current_price = binance_client.average_price(ticket_1, ticket_2)
        logging.info(current_price)

        if current_price == float(target):
            logging.info(f'WARNING PAIR {ticket_1}/{ticket_2} IN TAGRET ZONE = {target}!')
            break
        elif current_price == sub_target_low:
            logging.info(f'WARNING PAIR {ticket_1}/{ticket_2} NEAR TAGRET ZONE = {target}!')
            break
        elif current_price == sub_target_hight:
            logging.info(f'WARNING PAIR {ticket_1}/{ticket_2} NEAR TAGRET ZONE = {target}!')
            break


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
