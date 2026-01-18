from .models import Medicao
from .tasks import task_verificar_alerta_temperatura


def registrar_nova_medicao(aparelho, temperatura, umidade=None):
    """
    Registra a medição no banco e dispara a tarefa do Celery.
    """
    # Cria a medição no banco de dados (Postgres)
    medicao = Medicao.objects.create(
        aparelho=aparelho,
        temperatura=temperatura,
        umidade=umidade
    )

    # Dispara a tarefa assíncrona do Celery passando o ID do sensor
    # Certifique-se que o seu modelo Aparelho tem um campo 'sensor' ou similar
    if hasattr(aparelho, 'sensor'):
        task_verificar_alerta_temperatura.delay(aparelho.sensor.id, temperatura)

    return medicao