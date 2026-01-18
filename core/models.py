from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class Loja(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"
        ordering = ["nome"]


class User(AbstractUser):
    ADMIN = "ADMIN"
    TECNICO = "TECNICO"
    CLIENTE = "CLIENTE"

    ROLE_CHOICES = [
        (ADMIN, "Administrador"),
        (TECNICO, "Técnico"),
        (CLIENTE, "Cliente"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    loja = models.ForeignKey(
        Loja, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios"
    )
    tecnico_autorizado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self) -> str:
        return self.username


class Aparelho(models.Model):
    AR_CONDICIONADO = "AR"
    FREEZER = "FR"
    CAMARA_FRIA = "CF"

    TIPO_CHOICES = [
        (AR_CONDICIONADO, "Ar-condicionado"),
        (FREEZER, "Freezer"),
        (CAMARA_FRIA, "Câmara Fria"),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="aparelhos")
    mac_address = models.CharField(
        max_length=17, unique=True, null=True, blank=True,
        help_text="Endereço MAC do hardware (Ex: AA:BB:CC:11:22:33)"
    )

    # --- Validação de Limites ---
    temp_min = models.FloatField(default=2.0, help_text="Temperatura mínima aceitável")
    temp_max = models.FloatField(default=8.0, help_text="Temperatura máxima aceitável")

    # --- Monitoramento de Conectividade ---
    ultima_comunicacao = models.DateTimeField(null=True, blank=True, help_text="Último sinal recebido do ESP32")

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def status_conexao(self):
        """Retorna se o dispositivo está online com base nos últimos 10 minutos."""
        if not self.ultima_comunicacao:
            return "OFFLINE"

        limite = timezone.now() - timedelta(minutes=10)
        return "ONLINE" if self.ultima_comunicacao > limite else "OFFLINE"

    def __str__(self):
        return f"{self.nome} ({self.mac_address}) - {self.loja.nome}"

    class Meta:
        verbose_name = "Aparelho"
        verbose_name_plural = "Aparelhos"