import pymongo
from pymongo import MongoClient

maxServerDelay = 10
try:
    client = MongoClient(serverSelectionTimeoutMS=maxServerDelay)
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as error:
    print('mongo server error: {}'.format(error.message))

