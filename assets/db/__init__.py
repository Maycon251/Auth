from pymongo import MongoClient
from hashlib import md5
from os import getenv

try:
    client = MongoClient(getenv('MONGO_URI'))
    db = client.get_database('AuthDB')
except:
    print('Falha ao conectar ao banco de dados')
    exit()
