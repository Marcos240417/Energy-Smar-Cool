from django.contrib import admin
from .models import Sensor, Loja

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco']
    search_fields = ['nome']

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    # Alterado 'store_id' para 'loja'
    list_display = ['name', 'code', 'loja', 'is_active', 'min_temperature', 'max_temperature', 'created_at']
    list_filter = ['is_active', 'loja', 'device_type', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Location', {
            'fields': ('loja',) # Alterado aqui também
        }),
        ('Settings', {
            'fields': ('min_temperature', 'max_temperature', 'device_type', 'ip_address')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )