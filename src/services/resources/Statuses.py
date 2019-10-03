import flask_restful
from pymongo import MongoClient

from src.services.utlis.JSONEncoder import JSONEncoder


class StatusList(flask_restful.Resource):
    def __init__(self, configs):
        self.mongoClient = MongoClient(configs.mongodb_config['url'])
        self.collection = self.mongoClient[configs.mongodb_config['database']][configs.mongodb_config['collection']]
        self.jsonEncoder = JSONEncoder()

    def get(self, sinceTimestamp: float = None, untilTimestamp: float = None, limit: int = 100):
        if sinceTimestamp is not None and untilTimestamp is not None:
            return self.jsonEncoder.decode_to_dict(
                list(self.collection.find({"timestamp": {"$gt": sinceTimestamp, "$lt": untilTimestamp}}).limit(limit)))
        elif sinceTimestamp is not None:
            return self.jsonEncoder.decode_to_dict(
                list(self.collection.find({"timestamp": {"$gt": sinceTimestamp}}).limit(limit)))

        return self.jsonEncoder.decode_to_dict((self.collection.find({}).limit(100)))

    def __del__(self):
        self.mongoClient.close()


