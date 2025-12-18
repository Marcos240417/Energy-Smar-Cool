from django.db import models
from django.contrib.auth.models import AbstractUser

#Apenas para não me esquecer
#Usuário: admin
#Endereço de email:
#Password: 123
#Password (again): 123
#http://localhost:8000/admin
#http://localhost:8000/api/users/


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

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )

    loja = models.ForeignKey(
        Loja,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuarios",
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
    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="aparelhos"
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.loja.nome}"
