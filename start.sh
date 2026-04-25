#!/bin/bash

# start celery in background
celery -A origin.procure_ai.celery_worker worker --pool=solo --loglevel=info &

# start fastapi (THIS fixes Render port error)
uvicorn origin.procure_ai.main:app --host 0.0.0.0 --port 10000

apt-get update && apt-get install -y tesseract-ocr