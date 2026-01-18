import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoolSense.settings')
django.setup()

from core.models import Aparelho
from medicoes.models import Medicao
from alertas.models import Alerta
from django.utils import timezone


def simular_retorno_sensor(termo_busca):
    print(f"--- Buscando aparelho que contenha: '{termo_busca}' ---")

    # Busca flexível pelo nome
    aparelho = Aparelho.objects.filter(nome__icontains=termo_busca).first()

    if aparelho:
        # 1. Registrar medição
        Medicao.objects.create(
            aparelho=aparelho,
            temperatura=2.5,
            umidade=45.0,
            registrada_em=timezone.now()
        )
        print(f"✅ Medição registrada para: {aparelho.nome}")

        # 2. Resolver alertas
        # Buscamos alertas ativos que mencionem este aparelho no título ou mensagem
        alertas_resolvidos = Alerta.objects.filter(
            titulo__icontains=aparelho.nome,
            ativo=True
        ).update(ativo=False)

        print(f"✅ {alertas_resolvidos} alerta(s) resolvido(s).")
    else:
        print("❌ Erro: Nenhum aparelho encontrado.")
        print("Nomes disponíveis no banco:", list(Aparelho.objects.values_list('nome', flat=True)))


if __name__ == "__main__":
    simular_retorno_sensor("Freezer")