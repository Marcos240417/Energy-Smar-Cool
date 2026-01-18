from pymongo import MongoClient
from django.conf import settings


# ================================
# CONEXÃO COM MONGODB
# ================================
client = MongoClient(settings.MONGO_URI)
db = client["coolsense"]


# ================================
# MEDIÇÕES (TIME SERIES)
# ================================
def inserir_medicao(loja_id, sensor_id, temperatura):
    """
    Insere uma medição de temperatura no MongoDB.
    """
    return db.medicoes.insert_one(
        {
            "loja_id": loja_id,
            "sensor_id": sensor_id,
            "temperatura": temperatura,
        }
    )


def buscar_medicoes_por_loja(loja_id):
    """
    Retorna todas as medições de uma loja específica.
    """
    return db.medicoes.find({"loja_id": loja_id})
