worker: python main.py $PORT
celery_worker: celery -A tasks worker -l INFO
celery_beat: celery beat tasks -l INFO
