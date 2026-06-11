from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "app.tasks.scraper.scrape_amazon_dummy": "main-queue",
}

celery_app.conf.beat_schedule = {
    "scrape-amazon-every-hour": {
        "task": "app.tasks.scraper.scrape_amazon_dummy",
        "schedule": 3600.0, # every hour
    },
}

celery_app.autodiscover_tasks(["app.tasks.scraper"])
