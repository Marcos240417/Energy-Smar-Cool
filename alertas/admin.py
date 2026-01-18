from django.contrib import admin
from .models import Alerta

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "nivel", "ativo", "criado_em")
    list_filter = ("nivel", "ativo")
    search_fields = ("titulo", "mensagem")
