from pathlib import Path
import os
from datetime import timedelta
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# SECURITY (Use Variáveis de Ambiente em Produção)
# ================================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-dev-key")
DEBUG = os.environ.get("DEBUG", "1") == "1"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "web"]

# ================================
# APPLICATIONS
# ================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Bibliotecas de Terceiros
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "drf_spectacular",
    "corsheaders",  # ADICIONADO: Necessário para comunicação com App/Web

    # Seus Apps
    "core",
    "sensors",
    "alertas",
    "medicoes",
]

# ================================
# MIDDLEWARE
# ================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware", # DEVE vir antes do CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True # Para desenvolvimento. Em produção, especifique as URLs.

# ================================
# DATABASE (POSTGRES)
# ================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "mydb"),
        "USER": os.environ.get("POSTGRES_USER", "myuser"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "mypassword"),
        "HOST": os.environ.get("POSTGRES_HOST", "db_postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# ================================
# REST FRAMEWORK & SWAGGER
# ================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "CoolSense API",
    "DESCRIPTION": "Monitoramento IoT de refrigeradores e máquinas compatíveis.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ================================
# CELERY & REDIS
# ================================
CELERY_BROKER_URL = 'redis://localhost:6380/0' if os.name == 'nt' else 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TIMEZONE = "America/Recife"

CELERY_BEAT_SCHEDULE = {
    'verificar-sensores-offline-cada-5-min': {
        'task': 'medicoes.tasks.verificar_aparelhos_offline',
        'schedule': crontab(minute='*/5'),
    },
}

# ================================
# EMAIL CONFIG
# ================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'marcosrbterto@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD", "marcos2404") # Use env var!

# Restante das configs (I18N, STATIC, etc) permanecem as mesmas.
AUTH_USER_MODEL = "core.User"
ROOT_URLCONF = "CoolSense.urls"
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_TZ = True