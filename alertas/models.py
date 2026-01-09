from django.db import models

class Alerta(models.Model):
    NIVEIS = [
        ('info', 'Informativo'),
        ('warning', 'Aviso'),
        ('critical', 'Crítico'),
    ]

    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVEIS)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.nivel.upper()}] {self.titulo}"
