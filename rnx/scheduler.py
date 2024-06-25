import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functions import run_asyncio_job, create_services
from download_info import get_info

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: run_asyncio_job(get_info), 'cron', hour=23, minute=0)
    scheduler.add_job(lambda: run_asyncio_job(create_services), 'cron', hour=0, minute=0)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass