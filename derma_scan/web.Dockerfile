FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY wait_for_db.py /app/wait_for_db.py

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "movie_website.wsgi:application", "--bind", "0.0.0.0:8000"]