from datetime import datetime
from pymongo import MongoClient

from src.services.Logger import Logger


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
        date = datetime.now().timestamp()

        data['timestamp'] = date

        print(data)

        collection.insert_one(data)

    def __del__(self):
        self.mongodb.close()
