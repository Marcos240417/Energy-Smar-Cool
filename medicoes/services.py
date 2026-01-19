from .models import Medicao
from .tasks import task_verificar_alerta_temperatura


def registrar_nova_medicao(aparelho, temperatura, umidade=None):

    medicao = Medicao.objects.create(
        aparelho=aparelho,
        temperatura=temperatura,
        umidade=umidade
    )

    if hasattr(aparelho, 'sensor'):
        task_verificar_alerta_temperatura.delay(aparelho.sensor.id, temperatura)

    return medicao