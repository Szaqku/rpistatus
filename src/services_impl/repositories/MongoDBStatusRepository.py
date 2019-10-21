from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from src.services.repositories.Respository import Repository
from src.services.utlis.JSONEncoder import JSONEncoder


class MongoDBStatusRepository(Repository):
    
    def __init__(self, mongoClient: MongoClient, databaseName, collectionName):
        self.collectionName = collectionName
        self.databaseName = databaseName
        self.mongoClient = mongoClient
        self.jsonEncoder = JSONEncoder

    def get(self, filters: dict):
        try:
            return list(self.jsonEncoder().encode(self.mongoClient[self.databaseName][self.collectionName].find(filters)))
        except ServerSelectionTimeoutError as ex:
            print("Error happened while inserting data. ", ex)
            return []

    def create(self, data: dict):
        try:
            self.mongoClient[self.databaseName][self.collectionName].insert_one(data)
        except ServerSelectionTimeoutError as ex:
            print("Error happened while inserting data. ", ex)

    def delete(self, filters: dict):
        self.mongoClient[self.databaseName][self.collectionName].delete_one(filters)
