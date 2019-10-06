
from pymongo import MongoClient

from src.services.Respository import Repository
from src.services.utlis.JSONEncoder import JSONEncoder


class MongoDBStatusRepository(Repository):
    
    def __init__(self, mongoClient: MongoClient, databaseName, collectionName):
        self.collectionName = collectionName
        self.databaseName = databaseName
        self.mongoClient = mongoClient
        self.jsonEncoder = JSONEncoder

    def get(self, filters: dict):
        return list(self.jsonEncoder().encode(self.mongoClient[self.databaseName][self.collectionName].find(filters)))

    def create(self, data: dict):
        self.mongoClient[self.databaseName][self.collectionName].insert_one(data)

    def delete(self, filters: dict):
        self.mongoClient[self.databaseName][self.collectionName].delete_one(filters)
