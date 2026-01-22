
#!/bin/sh
set -e

echo "Iniciando o ambiente na Railway..."

# Rodar migrações para garantir que o banco tenha as tabelas
python manage.py migrate --noinput

# Coletar arquivos estáticos (necessário para WhiteNoise)
python manage.py collectstatic --noinput

echo "Banco de dados atualizado e arquivos estáticos coletados!"

exec "$@"
