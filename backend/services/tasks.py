"""
Celery tasks for scheduled content processing
"""
from celery import Celery
from celery.schedules import crontab
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from services.content_processor import ContentProcessor
from database.connection import SessionLocal

# Initialize Celery
celery_app = Celery(
    'hr_signals',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task(name='scrape_and_process_content')
def scrape_and_process_content():
    """
    Scheduled task to scrape and process new content
    """
    print("Starting scheduled content processing...")

    processor = ContentProcessor()
    result = asyncio.run(processor.scrape_and_process_all())

    return result


@celery_app.task(name='generate_daily_digest')
def generate_daily_digest():
    """
    Generate daily digest
    """
    print("Generating daily digest...")

    db = SessionLocal()
    try:
        processor = ContentProcessor()
        digest = asyncio.run(processor.generate_daily_digest(db))

        if digest:
            return {"status": "success", "digest_id": digest.id}
        else:
            return {"status": "no_content"}

    finally:
        db.close()


@celery_app.task(name='generate_weekly_digest')
def generate_weekly_digest():
    """
    Generate weekly digest
    """
    print("Generating weekly digest...")

    # Similar to daily digest but for weekly period
    # Implementation would follow similar pattern

    return {"status": "success"}


@celery_app.task(name='cleanup_old_data')
def cleanup_old_data():
    """
    Clean up old data (optional maintenance task)
    """
    from datetime import datetime, timedelta

    db = SessionLocal()
    try:
        # Example: Archive articles older than 1 year
        one_year_ago = datetime.utcnow() - timedelta(days=365)

        # Could move to archive table or mark as archived
        # For now, just log
        from models.database import Article
        old_count = db.query(Article)\
            .filter(Article.published_date < one_year_ago)\
            .count()

        print(f"Found {old_count} old articles")

        return {"status": "success", "old_articles": old_count}

    finally:
        db.close()


# Scheduled tasks configuration
celery_app.conf.beat_schedule = {
    'scrape-every-6-hours': {
        'task': 'scrape_and_process_content',
        'schedule': crontab(minute=0, hour='*/6'),  # Every 6 hours
    },
    'daily-digest': {
        'task': 'generate_daily_digest',
        'schedule': crontab(minute=0, hour=8),  # 8 AM daily
    },
    'weekly-digest': {
        'task': 'generate_weekly_digest',
        'schedule': crontab(minute=0, hour=9, day_of_week=1),  # Monday 9 AM
    },
    'cleanup-monthly': {
        'task': 'cleanup_old_data',
        'schedule': crontab(minute=0, hour=2, day_of_month=1),  # First day of month, 2 AM
    },
}


if __name__ == '__main__':
    celery_app.start()
