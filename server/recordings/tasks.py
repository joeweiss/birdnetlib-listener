from huey import crontab
from huey.contrib.djhuey import task, lock_task, periodic_task
import os
import requests

# This is a scheduled version of the extractor. It's basically a backup.
@periodic_task(crontab(minute="*/10", hour="5-23"))
@lock_task("push-lock")  # Goes *after* the task decorator.
def run_push_to_tidbyt_app():
    response = requests.get(
        "http://web:8000/latest/"
    )  # Cache the response before calling pixlets.
    os.system("cd /usr/src/app/pixlets/; sh push-install.sh")
