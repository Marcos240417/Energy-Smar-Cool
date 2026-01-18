# 🚀 DevCycle – Guia de Desenvolvimento Diário

Guia oficial para o fluxo de desenvolvimento, boas práticas, comandos úteis e padronizações da equipe.

Este documento foi criado para garantir que todos os membros da equipe sigam o mesmo padrão no dia a dia, evitando problemas e aumentando a produtividade.

---

## 📌 Índice

1.  [💡 Filosofia do Desenvolvimento](#-filosofia-do-desenvolvimento)
2.  [🧩 Branches](#-branches)
3.  [🔄 Fluxo de Git](#-fluxo-de-git)
4.  [🚀 Commits](#-commits)
5.  [🐳 Rotina com Docker](#-rotina-com-docker)
6.  [🎯 Rotina com Django / Backend](#-rotina-com-django--backend)
7.  [📦 Banco de Dados (Postgres & Mongo)](#-banco-de-dados-postgres--mongo)
8.  [🧪 Testes](#-testes)
9.  [⚠️ Erros Comuns e Soluções](#-erros-comuns-e-soluções)
10. [📚 Snippets (códigos prontos)](#-snippets-códigos-prontos)
11. [🤝 Contribuição](#-contribuição)
12. [🎉 Finalização](#-finalização)

---

## 💡 Filosofia do Desenvolvimento

Nossa filosofia é baseada nos seguintes princípios:

*   **Código limpo** > código rápido
*   **Pequenas entregas** > grandes features incompletas
*   **Automação** > tarefas manuais repetitivas
*   **Ambiente Docker** sempre funcionando

**Sempre valide antes de abrir um Pull Request (PR):**

*   ✔ Funciona local
*   ✔ Testes passam
*   ✔ Código padronizado
*   ✔ Commit explicativo
*   ✔ Merge simples

## 🧩 Branches

Utilizamos o padrão **GitHub Flow** com as seguintes convenções de nomenclatura:

| Tipo | Prefixo | Exemplo | Uso |
| :--- | :--- | :--- | :--- |
| **Main** | `main` | `main` | Produção / Deploy |
| **Feature** | `feature/` | `feature/nome-feature` | Novas funcionalidades |
| **Fix** | `fix/` | `fix/descrição` | Correções rápidas |
| **Refactor** | `refactor/` | `refactor/motivo` | Melhoria de código sem alterar regras de negócio |
| **Hotfix** | `hotfix/` | `hotfix/bug` | Correção urgente em produção |

## 🔄 Fluxo de Git

Siga os passos abaixo para um fluxo de trabalho padronizado:

1.  **Criar nova branch:**
    ```bash
    git checkout -b feature/nome-da-sua-feature
    ```

2.  **Puxar atualizações antes de começar a trabalhar:**
    ```bash
    git pull origin main
    ```

3.  **Adicionar alterações:**
    ```bash
    git add .
    ```

4.  **Commit (seguindo o padrão Conventional Commits):**
    ```bash
    git commit -m "feat: adiciona endpoint de criação de usuário"
    ```

5.  **Enviar branch:**
    ```bash
    git push origin feature/nome-da-sua-feature
    ```

6.  **Abrir Pull Request (PR):**
    O PR deve ser **pequeno**, **objetivo** e ter uma **descrição clara**.

## 🚀 Commits

Utilizamos o padrão **Conventional Commits** para manter um histórico limpo e legível.

| Prefixo | Uso |
| :--- | :--- |
| `feat:` | Nova feature |
| `fix:` | Correção de bug |
| `docs:` | Alterações na documentação |
| `refactor:` | Melhorias internas sem mudança de funcionalidade |
| `test:` | Adição ou correção de testes |
| `chore:` | Manutenção, build, ou tarefas de rotina |

**Exemplos:**

*   `feat: implementa autenticação com JWT`
*   `fix: corrige conexão com banco postgres`
*   `docs: adiciona instruções de setup local`

## 🐳 Rotina com Docker

Comandos essenciais para o dia a dia com Docker Compose:

| Comando | Descrição |
| :--- | :--- |
| `docker compose up --build` | Sobe todos os serviços e reconstrói as imagens. |
| `docker compose up -d` | Sobe todos os serviços em *background* (modo *detached*). |
| `docker compose down` | Para e remove os containers. |
| `docker compose logs -f web` | Acompanha os logs do serviço `web` (Django) em tempo real. |
| `docker compose build --no-cache` | Força a reconstrução completa das imagens, ignorando o cache. |
| `docker exec -it nome_do_container bash` | Acessa o terminal de um container específico (ex: `web`, `db_postgres`). |

## 🎯 Rotina com Django / Backend

Comandos comuns para o desenvolvimento com Django:

| Comando | Descrição |
| :--- | :--- |
| `docker compose exec web python manage.py migrate` | Aplica as migrações pendentes no banco de dados. |
| `docker compose exec web python manage.py makemigrations` | Cria novos arquivos de migração com base nas alterações dos modelos. |
| `docker compose exec web python manage.py createsuperuser` | Cria um usuário administrador para o Django Admin. |
| `docker compose exec web python manage.py shell` | Abre o *shell* interativo do Django dentro do container. |
| `find . -name "__pycache__" -exec rm -rf {} +` | Limpa arquivos de cache (`__pycache__`) do Python. |

## 📦 Banco de Dados (Postgres & Mongo)

Comandos para acesso e gerenciamento dos bancos de dados:

| Comando | Descrição |
| :--- | :--- |
| `docker compose exec db_postgres psql -U $POSTGRES_USER -d $POSTGRES_DB` | Acessa o terminal `psql` do PostgreSQL. |
| `docker compose exec mongo mongosh` | Acessa o *shell* do MongoDB. |
| `docker compose down -v` | **Reseta** o banco de dados PostgreSQL (para e apaga o volume de dados). |

## 🧪 Testes

| Comando | Descrição |
| :--- | :--- |
| `docker compose exec web pytest` | Roda todos os testes da aplicação. |
| `docker compose exec web pytest --cov` | Roda os testes e gera o relatório de cobertura de código. |

## ⚠️ Erros Comuns e Soluções

| Erro | Causa Comum | Solução |
| :--- | :--- | :--- |
| `sh: wait_for_db.sh: not found` | O script não foi copiado ou não está no `PATH` do container. | Ajustar o `Dockerfile` para copiar o script corretamente. |
| `port is already allocated` | A porta (ex: 8000) já está sendo usada por outro processo na sua máquina. | Matar o processo que está usando a porta ou alterar a porta no `docker-compose.yml`. |
| `could not connect to database` | O banco de dados não subiu a tempo ou o serviço não está acessível. | Garantir o uso de `depends_on` e do script `wait_for_db.sh`. |
| `ModuleNotFoundError` | Uma dependência do Python está faltando. | Executar `docker compose build --no-cache` para reconstruir a imagem. |
| `permission denied` em `.sh` | O script não tem permissão de execução. | Adicionar `RUN chmod +x script.sh` no `Dockerfile`. |

## 📚 Snippets (Códigos Prontos)

### Exemplo de Conexão PostgreSQL no `settings.py`

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": "db_postgres", # Nome do serviço no docker-compose
        "PORT": 5432,
    }
}
```

### Exemplo de Espera pelo Banco (`wait_for_db.sh`)

```bash
#!/bin/sh

echo "⏳ Aguardando o Postgres iniciar..."

while ! nc -z db_postgres 5432; do
  sleep 0.5
done

echo "🚀 Postgres disponível!"
# Adicionar lógica para o Mongo aqui, se necessário

exec "$@"
```

### Outros Comandos Úteis

*   **Rodar servidor Django manualmente:**
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
*   **Rodar lint (Python):**
    ```bash
    flake8 .
    ```

## 🤝 Contribuição

Para contribuir com o projeto, siga estas diretrizes:

*   Sempre crie **Pull Requests (PRs) curtos** e focados em uma única tarefa.
*   **Não envie commits diretamente para a branch `main`**.
*   Revise o código dos colegas de equipe com atenção e forneça *feedback* construtivo.
*   Evite grandes mudanças estruturais sem discussão prévia com o time.

## 🎉 Finalização

Com este guia, sua equipe terá uma padronização clara para trabalhar com:

*   Docker
*   Django
*   Postgres & Mongo
*   Git
*   Commits
*   Branching
*   Testes
*   Fluxo diário
