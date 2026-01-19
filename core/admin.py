from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Loja
from .models import Aparelho


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "cnpj", "ativa")
    search_fields = ("nome", "cnpj")
    list_filter = ("ativa",)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Informações do Sistema", {
            "fields": ("role", "loja", "tecnico_autorizado"),
        }),
    )

    list_display = (
        "username",
        "email",
        "role",
        "loja",
        "tecnico_autorizado",
        "is_staff",
        "is_active",
    )

    list_filter = ("role", "is_active", "tecnico_autorizado")


@admin.register(Aparelho)
class AparelhoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "tipo", "loja", "ativo")
    list_filter = ("tipo", "ativo")
    search_fields = ("nome", "loja__nome")

