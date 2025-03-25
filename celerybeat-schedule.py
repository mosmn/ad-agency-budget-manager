from celery import Celery
from celery.schedules import crontab

app = Celery('ad_agency_scheduler')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
)

# Set up the periodic tasks
app.conf.beat_schedule = {
    'reset-daily-budgets': {
        'task': 'celery_tasks.reset_daily_budgets',
        'schedule': crontab(hour=0, minute=0),  # Run at midnight every day
    },
    'reset-monthly-budgets': {
        'task': 'celery_tasks.reset_monthly_budgets',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),  # Run on the 1st of every month
    },
    'check-campaign-status-hourly': {
        'task': 'celery_tasks.check_campaign_status',
        'schedule': crontab(minute=0),  # Run every hour
    },
}

app.conf.timezone = 'UTC'
