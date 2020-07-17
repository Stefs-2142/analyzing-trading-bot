from binance_utils import BinanceClient
from celery import Celery
import logging
from time import sleep


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
