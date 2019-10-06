from pymongo import MongoClient

from src.services.loggers.Logger import Logger


class MongoDBLogger(Logger):
    mongodb: MongoClient
    database: str
    collection: str

    def __init__(self, mongoClient: MongoClient, database: str = "test", collection: str = "rpistatus"):
        self.collection = collection
        self.database = database
        self.mongodb = mongoClient

    def log(self, data: dict):
        collection = self.mongodb[self.database][self.collection]
        collection.insert_one(data.copy())

    def __del__(self):
        self.mongodb.close()