
set -e

echo " Aguardando Postgres (db_postgres:5432)..."
until nc -z db_postgres 5432; do
  sleep 1
done
echo " Postgres disponível!"

echo " Aguardando MongoDB (mongo:27017)..."
until nc -z mongo 27017; do
  sleep 1
done
echo " MongoDB disponível!"

exec "$@"
