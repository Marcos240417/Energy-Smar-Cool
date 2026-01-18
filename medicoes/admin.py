from django.contrib import admin
from .models import Medicao

@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = ("aparelho", "temperatura", "umidade", "registrada_em")
    list_filter = ("aparelho",)
    search_fields = ("aparelho__nome",)
