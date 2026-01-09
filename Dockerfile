FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    gcc \
    python3-dev \
    musl-dev \
 && rm -rf /var/lib/apt/lists/*

COPY wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "/wait_for_db.sh && python manage.py runserver 0.0.0.0:8000"]
