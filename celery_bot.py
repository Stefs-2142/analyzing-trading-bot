from settings import BACKEND_PATH, BROKER_PATH

from celery import Celery
from celery.schedules import crontab


app = Celery(
    'celery',
    broker=BROKER_PATH,
    backend=BACKEND_PATH,
)

app.conf.update(
    result_expires=3600
)

app.conf.beat_schedule = {
    # В планировщике задач прописываем 2 таска:
    # 1-ый beat_crypto_booling раз в 5 минут.
    # 2-ой beat_classic_booling раз в 5 минут.
    'checking-crypto-price-every-5-min': {
        'task': 'tasks.beat_crypto_pooling',
        'schedule': crontab(minute='*/5')
    },
    'checking-classic-price-every-5-min': {
        'task': 'tasks.beat_classic_pooling',
        'schedule': crontab(minute='*/5')
    },
}

if __name__ == '__main__':
    app.start()
