import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoolSense.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Loja, Aparelho

User = get_user_model()

def run_seed():
    print("--- Iniciando Seed do Banco de Dados ---")

    # 1. Criar Lojas com CNPJs fictícios para evitar erro de IntegrityError
    loja1, _ = Loja.objects.get_or_create(
        cnpj="12345678000101",
        defaults={"nome": "Mercado Central", "ativa": True}
    )
    loja2, _ = Loja.objects.get_or_create(
        cnpj="98765432000102",
        defaults={"nome": "Farmácia Recife", "ativa": True}
    )
    print("✅ Lojas criadas (ou já existentes).")

    # 2. Criar Usuários
    users_data = [
        {"username": "admin_master", "role": "ADMIN", "email": "admin@coolsense.com"},
        {"username": "tecnico_joao", "role": "TECNICO", "email": "joao@tech.com"},
        {"username": "dono_mercado", "role": "CLIENTE", "email": "dono@mercado.com", "loja": loja1},
        {"username": "dono_farmacia", "role": "CLIENTE", "email": "dono@farmacia.com", "loja": loja2},
    ]

    for data in users_data:
        if not User.objects.filter(username=data["username"]).exists():
            loja = data.pop("loja", None)
            user = User.objects.create_user(**data, password="senha123")
            if loja:
                user.loja = loja
                user.save()
            print(f"👤 Usuário {data['username']} ({data['role']}) criado.")
        else:
            print(f"⏩ Usuário {data['username']} já existe.")

        # 3. Criar Aparelhos (Usando o campo 'nome' para busca)
        Aparelho.objects.get_or_create(
            nome="Freezer Carnes",
            defaults={"loja": loja1, "tipo": "FREEZER"}  # Ajuste o tipo se necessário
        )
        Aparelho.objects.get_or_create(
            nome="Geladeira Vacinas",
            defaults={"loja": loja2, "tipo": "GELADEIRA"}
        )
        print("✅ Aparelhos vinculados.")

        print("--- Seed finalizado com sucesso! ---")

    if __name__ == "__main__":
        run_seed()