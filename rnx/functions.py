import asyncio
from datetime import date, timedelta
import subprocess


async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f"Error running command {command}: {stderr.decode().strip()}")
    return stdout, stderr

def run_asyncio_job(job):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(job())
    loop.close()

def create_services():
    run_command(f'sudo create_services.py {(date.today() - timedelta(days=2)).strftime("%Y-%d-%m")}')