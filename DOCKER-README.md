# 📘 CoolSense — Ambiente Dockerizado (Django + Postgres + MongoDB)

Este projeto utiliza **Django**, **PostgreSQL**, **MongoDB** e **Docker** para criar um ambiente de desenvolvimento padronizado para toda a equipe.

Abaixo está a explicação completa da arquitetura, dos serviços e da configuração realizada.

---

## 📌 Arquitetura Geral

O sistema é composto pelos seguintes serviços:

*   **Django**: Aplicação principal (backend).
*   **PostgreSQL**: Banco de dados relacional utilizado pelo Django.
*   **MongoDB**: Banco de dados NoSQL para armazenamento adicional.
*   **Docker + Docker Compose**: Ferramentas de orquestração dos serviços.
*   **`wait_for_db.sh`**: Script que garante que o Django só inicie após o PostgreSQL e o MongoDB estarem completamente inicializados.

A aplicação sobe todos os serviços automaticamente com o comando:

```bash
docker-compose up --build
```

## 📁 Estrutura de Arquivos Relevante

A estrutura de arquivos principal é a seguinte:

```
CoolSense/
 ├ CoolSense/          # pasta principal do Django
 ├ core/               # app principal
 ├ wait_for_db.sh      # script para aguardar os bancos
 ├ dockerfile
 ├ docker-compose.yml
 ├ manage.py
 ├ requirements.txt
 └ .env
```

## 🐳 Detalhes da Configuração Docker

### `dockerfile` — Construção da Imagem do Django

O `dockerfile` cria a imagem da aplicação Django (`web`):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    gcc \
    python3-dev \
    musl-dev \
 && rm -rf /var/lib/apt/lists/*

# Copia o script de espera dos bancos
COPY wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "/wait_for_db.sh python manage.py runserver 0.0.0.0:8000"]
```

**Principais Ações:**

*   Define a imagem base `python:3.11-slim`.
*   Instala dependências de sistema necessárias (como `netcat-openbsd` para o script de espera).
*   Copia e torna executável o script `wait_for_db.sh`.
*   Instala as dependências Python via `requirements.txt`.
*   Define o `CMD` para iniciar o Django **somente após** a execução bem-sucedida do `wait_for_db.sh`.

### `docker-compose.yml` — Orquestração dos Serviços

O Docker Compose levanta 3 serviços principais: `db_postgres`, `mongo` e `web`.

```yaml
version: "3.8"

services:
  db_postgres:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  mongo:
    image: mongo:6
    restart: always
    volumes:
      - mongo_data:/data/db
    ports:
      - "27017:27017"

  web:
    build: .
    command: >
      sh -c "/wait_for_db.sh &&
             python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - ./:/app
    ports:
      - "8000:8000"
    depends_on:
      - db_postgres
      - mongo
    env_file:
      - .env

volumes:
  postgres_data:
  mongo_data:
```

**Principais Ações:**

*   Cria containers isolados para cada serviço.
*   Persiste os dados dos bancos de dados via volumes (`postgres_data` e `mongo_data`).
*   O serviço `web` depende de `db_postgres` e `mongo`.
*   O `command` do serviço `web` garante que as migrações (`migrate`) sejam executadas e o servidor Django seja iniciado **após** a verificação do `wait_for_db.sh`.
*   Expõe a aplicação em `http://localhost:8000/`.

### 🕒 Script `wait_for_db.sh`

Este script utiliza o comando `nc` (netcat) para evitar erros de inicialização do Django antes que os bancos de dados estejam prontos para aceitar conexões.

```bash
#!/bin/sh

# Espera o Postgres
until nc -z -v -w30 db_postgres 5432
do
  echo "Waiting for Postgres..."
  sleep 1
done

# Espera o Mongo
until nc -z -v -w30 mongo 27017
do
  echo "Waiting for Mongo..."
  sleep 1
done

echo "Databases are up!"
exec "$@"
```

**Função:**

*   Testa a conexão com o PostgreSQL na porta `5432` do host `db_postgres`.
*   Testa a conexão com o MongoDB na porta `27017` do host `mongo`.
*   Somente após a confirmação de ambas as conexões, executa o comando principal do Django (`exec "$@"`).

## ⚙️ Variáveis de Ambiente (`.env`)

O arquivo `.env` é lido pelo `docker-compose.yml` e contém as variáveis de configuração:

```ini
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword

MONGO_URI=mongodb://mongo:27017/coolsense
DJANGO_SECRET_KEY=mysecretkey
```

**Importante:** O Django lê essas variáveis dentro do seu arquivo `settings.py` para configurar as conexões.

## 🗄️ Integrações

### PostgreSQL

Configuração de exemplo no `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db_postgres", # Nome do serviço no docker-compose
        "PORT": 5432,
    }
}
```

### MongoDB (PyMongo)

Configuração de exemplo para acesso via PyMongo:

```python
from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["coolsense"]
```

**Observações:**

*   O MongoDB **não** é gerenciado pelo Django ORM.
*   Deve ser acessado diretamente via `mongo_db.minha_colecao`.

## ▶️ Como Subir o Projeto

1.  **Build da Aplicação**
    ```bash
    docker-compose build
    ```

2.  **Subir Todos os Serviços**
    ```bash
    docker-compose up
    ```

3.  **Acessar a Aplicação**
    A aplicação estará disponível em: `http://localhost:8000/`

## ▶️ Comandos Úteis

| Comando | Descrição |
| :--- | :--- |
| `docker-compose down` | Para todos os serviços. |
| `docker-compose down -v` | Para todos os serviços e apaga os volumes (reseta os bancos de dados). |
| `docker-compose exec web python manage.py migrate` | Executa as migrações do Django manualmente. |
| `docker-compose exec web sh` | Entra no terminal do container Django. |

## ✔️ Conclusão

Este setup garante:

*   **Ambiente padronizado** entre todos os desenvolvedores.
*   **Inicialização segura** graças ao `wait_for_db.sh`.
*   **Migrations automáticas** no startup.
*   **Hot reload** via bind-volume (`.:/app`).
*   Melhor produtividade e segurança.
