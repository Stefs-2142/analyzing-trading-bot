worker: cd atbbot && python main.py $PORT
worker_celery: cd atbbot && python -m celery -A tasks worker -l INFO
worker_celery_beat: cd atbbot && python -m celery -A tasks beat -l INFO

