from celery import Celery
from time import sleep
import logging


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


celery = make_celery()


@celery.task
def alert_status(ticket_1, ticket_2, target):

    from client_app import binance_client

    three_percent = 0.03
    sub_target_low = round((target - target * three_percent), 1)  # Зададём границы таргета в 3%
    sub_target_hight = round((target + target * three_percent), 1)

    while True:
        sleep(5)
        current_price = binance_client.average_price(ticket_1, ticket_2)

        if current_price == float(target):
            logging.info(f'WARNING PAIR {ticket_1}/{ticket_2} IN TAGRET ZONE = {target}!')
            break
        elif current_price == sub_target_low:
            logging.info(f'WARNING PAIR {ticket_1}/{ticket_2} NEAR TAGRET ZONE = {target}!')
            break
        elif current_price == sub_target_hight:
            logging.info(f'WARNING PAIR {ticket_1}/{ticket_2} NEAR TAGRET ZONE = {target}!')
            break
