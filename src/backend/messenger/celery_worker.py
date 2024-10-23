from celery import Celery

from messenger.schema.user import User
from messenger.schema.message import Message
from messenger.settings import settings
import requests


celery = Celery(
    "worker",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}/0",
    backend=f"redis://{settings.redis_host}:{settings.redis_port}/0",
)


@celery.task
def send_notification(user: dict, text: str):
    url = f"https://api.telegram.org/bot{settings.bot_token}/sendMessage"
    payload = {
        "chat_id": user["telegram_id"],
        "text": text,
    }

    response = requests.post(url, data=payload)
