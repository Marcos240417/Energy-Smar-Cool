import os
from celery import Celery

# Certifique-se que o caminho aponta para seu arquivo de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoolSense.settings')

app = Celery('CoolSense')

# O namespace 'CELERY' significa que todas as configs no settings.py
# devem começar com CELERY_ (ex: CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Isso procura por tasks.py em todos os seus apps (medicoes, alertas, etc)
app.autodiscover_tasks()