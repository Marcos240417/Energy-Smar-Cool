from .models import Alerta
from .rules import REGRAS

def verificar_alertas(medicao):
    alertas_criados = []
    for regra in REGRAS:
        resultado = regra(medicao)
        if resultado:
            alerta = Alerta.objects.create(
                titulo=resultado["titulo"],
                mensagem=resultado["mensagem"],
                nivel=resultado["nivel"],
                ativo=True
            )
            alertas_criados.append(alerta)
    return alertas_criados
