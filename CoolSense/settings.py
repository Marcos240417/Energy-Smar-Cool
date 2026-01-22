from pathlib import Path
import os
import dj_database_url
from datetime import timedelta

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# SECURITY (Ajustado para Render)
# ================================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-chave-temporaria")
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Permite localhost e o domínio do Render
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "energy-smar-cool.onrender.com"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

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

    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "drf_spectacular",
    "corsheaders",  # Gerencia acesso do frontend externo

    "core",
    "sensors",      # Monitoramento térmico
    "alertas",
    "medicoes",
]

# ================================
# MIDDLEWARE (Incluindo WhiteNoise e CORS)
# ================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # Servir estáticos no Render
    "corsheaders.middleware.CorsMiddleware",       # Libera acesso à API
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Libera o acesso para que o outro desenvolvedor conecte o frontend dele
CORS_ALLOW_ALL_ORIGINS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CoolSense.wsgi.application'

# ================================
# DATABASE (Railway PostgreSQL)
# ================================
# Apenas se o erro persistir após ajustar a variável no Railway
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        engine='django.db.backends.postgresql' # Isso força o Django a usar o Postgres
    )
}

# ================================
# REST FRAMEWORK & AUTH
# ================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ================================
# STATIC FILES & CELERY
# ================================
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

AUTH_USER_MODEL = "core.User"
ROOT_URLCONF = "CoolSense.urls"
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
