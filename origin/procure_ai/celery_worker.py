import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "procure_ai",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# 🔥 IMPORTANT FIX FOR UPSTASH SSL
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,

    broker_use_ssl={
        "ssl_cert_reqs": "CERT_NONE"
    },
    redis_backend_use_ssl={
        "ssl_cert_reqs": "CERT_NONE"
    }
)