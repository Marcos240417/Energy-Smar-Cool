"""
Django settings for CoolSense project.
"""

from pathlib import Path
import os
from datetime import timedelta

# ================================
# BASE DIR
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ================================
# SECURITY
# ================================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-dev-key")

DEBUG = os.environ.get("DEBUG", "1") == "1"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "web",  # nome do serviço no Docker
]


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
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "core",
    "sensors",
    "alertas",
    "medicoes",
]

# ================================
# DJANGO REST FRAMEWORK + JWT
# ================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20, 
}

# ================================
# SIMPLE JWT CONFIG
# ================================
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# ================================
# AUTH USER
# ================================
AUTH_USER_MODEL = "core.User"


# ================================
# MIDDLEWARE
# ================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ================================
# URLS / WSGI
# ================================
ROOT_URLCONF = "CoolSense.urls"

WSGI_APPLICATION = "CoolSense.wsgi.application"


# ================================
# TEMPLATES
# ================================
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
# MONGO (APENAS URI)
# ================================
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://mongo:27017/coolsense"
)


# ================================
# PASSWORD VALIDATION
# ================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# ================================
# INTERNATIONALIZATION
# ================================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"

USE_I18N = True
USE_TZ = True


# ================================
# STATIC FILES
# ================================
STATIC_URL = "/static/"


# ================================
# DEFAULT PRIMARY KEY
# ================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

