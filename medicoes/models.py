from django.db import models
from core.models import Aparelho  # certifique-se que o modelo Aparelho existe em core.models

class Medicao(models.Model):
    aparelho = models.ForeignKey(
        Aparelho,
        on_delete=models.CASCADE,
        related_name="medicoes"
    )
    temperatura = models.FloatField()
    umidade = models.FloatField(null=True, blank=True)
    registrada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Medição"
        verbose_name_plural = "Medições"
        ordering = ["-registrada_em"]

    def __str__(self):
        return f"{self.aparelho.nome} - {self.temperatura}°C"
