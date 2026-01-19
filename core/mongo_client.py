from pymongo import MongoClient
from django.conf import settings


client = MongoClient(settings.MONGO_URI)
db = client["coolsense"]

def inserir_medicao(loja_id, sensor_id, temperatura):

    return db.medicoes.insert_one(
        {
            "loja_id": loja_id,
            "sensor_id": sensor_id,
            "temperatura": temperatura,
        }
    )


def buscar_medicoes_por_loja(loja_id):

    return db.medicoes.find({"loja_id": loja_id})
