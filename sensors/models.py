from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Loja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Sensor(models.Model):
    name = models.CharField(max_length=100, help_text="Sensor identifier name")
    code = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Unique sensor code (e.g., ESP32-001)"
    )
    description = models.TextField(blank=True, null=True, help_text="Sensor description")
    
    # Alterado de store_id para uma relação real com a classe Loja
    loja = models.ForeignKey(
        Loja, 
        on_delete=models.CASCADE, 
        related_name='sensores',
        help_text="Loja onde o sensor está instalado"
    )
    
    min_temperature = models.FloatField(
        default=-10.0,
        validators=[MinValueValidator(-50.0), MaxValueValidator(50.0)],
        help_text="Minimum acceptable temperature in °C"
    )
    max_temperature = models.FloatField(
        default=10.0,
        validators=[MinValueValidator(-50.0), MaxValueValidator(50.0)],
        help_text="Maximum acceptable temperature in °C"
    )
    
    is_active = models.BooleanField(default=True, help_text="Is sensor active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    device_type = models.CharField(
        max_length=50,
        default="ESP32",
        help_text="Device type (ESP32, ESP8266, etc.)"
    )
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text="Device IP address"
    )
    
    class Meta:
        db_table = 'sensors'
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensors'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
            models.Index(fields=['loja']), # Index atualizado para usar o novo campo
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def status_display(self):
        return "Active" if self.is_active else "Inactive"