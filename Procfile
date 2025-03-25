worker: cd src && celery -A celery_tasks worker --loglevel=info
scheduler: celery -A celerybeat-schedule beat --loglevel=info
sim: python src/main.py --simulate --spend 50
```
