import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functions import run_asyncio_job, create_services
from download_info import get_info

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: run_asyncio_job(get_info), 'cron', hour=5, minute=57)
    scheduler.add_job(lambda: run_asyncio_job(create_services), 'cron', hour=6, minute=35)
    scheduler.start()
    
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass