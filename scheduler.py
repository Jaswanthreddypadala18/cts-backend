from apscheduler.schedulers.background import BackgroundScheduler
import pytz

scheduler = BackgroundScheduler(timezone=pytz.UTC)

def start_scheduler():
    scheduler.start()
