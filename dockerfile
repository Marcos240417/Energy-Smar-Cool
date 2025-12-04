FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    gcc \
    python3-dev \
    musl-dev \
 && rm -rf /var/lib/apt/lists/*

COPY wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh


# Copia o arquivo de dependências Python e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "/app/wait_for_db.sh python manage.py runserver 0.0.0.0:8000"]
