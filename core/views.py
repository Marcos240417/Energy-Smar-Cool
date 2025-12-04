from django.shortcuts import render
from django.http import JsonResponse
from .mongo_client import db_mongo

def test_mongo(request):
    result = db_mongo.logs.insert_one({"msg": "Olá Mongo!"})
    return JsonResponse({"id": str(result.inserted_id)})

