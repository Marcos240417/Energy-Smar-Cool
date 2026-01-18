from django.db import models
from django.conf import settings

class Alerta(models.Model):
    NIVEIS = [
        ('info', 'Informativo'),
        ('warning', 'Aviso'),
        ('critical', 'Crítico'),
    ]

    # Relacionamento crucial para as estatísticas funcionarem
    aparelho = models.ForeignKey(
        'core.Aparelho',
        on_delete=models.CASCADE,
        related_name='alertas',
        null=True,
        blank=True
    )

    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVEIS)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.nivel.upper()}] {self.titulo}"

class AlertaLog(models.Model):
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE, related_name='logs')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Responsável"
    )
    observacao = models.TextField(verbose_name="O que foi feito?")
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ['-data_hora']

    def __str__(self):
        return f"Resolução de {self.alerta.titulo} por {self.usuario}"