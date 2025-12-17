FROM python:3.11-slim

# ================================
# WORKDIR
# ================================
WORKDIR /app


# ================================
# DEPENDÊNCIAS DO SISTEMA
# ================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    gcc \
    python3-dev \
    musl-dev \
 && rm -rf /var/lib/apt/lists/*


# ================================
# SCRIPT DE ESPERA DOS BANCOS
# ================================
COPY wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh


# ================================
# DEPENDÊNCIAS PYTHON
# ================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ================================
# CÓDIGO DA APLICAÇÃO
# ================================
COPY . .


# ================================
# PORTA
# ================================
EXPOSE 8000


# ================================
# START COMMAND
# ================================
CMD ["sh", "-c", "/wait_for_db.sh && python manage.py runserver 0.0.0.0:8000"]
