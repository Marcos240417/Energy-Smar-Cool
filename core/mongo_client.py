from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")

client = MongoClient(MONGO_URI)
db_mongo = client["cool_sense_db"]
