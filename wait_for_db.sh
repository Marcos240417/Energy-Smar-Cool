#!/bin/sh

# Espera o Postgres
until nc -z -v -w30 db_postgres 5432
do
  echo "Waiting for Postgres..."
  sleep 1
done

# Espera o Mongo
until nc -z -v -w30 mongo 27017
do
  echo "Waiting for Mongo..."
  sleep 1
done

echo "Databases are up!"
exec "$@"
