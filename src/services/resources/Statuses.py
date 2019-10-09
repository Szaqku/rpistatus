import flask_restful
from src.services.utlis.JSONEncoder import JSONEncoder
from src.services_impl.repositories.MongoDBStatusRepository import MongoDBStatusRepository


class StatusList(flask_restful.Resource):
    def __init__(self, repository: MongoDBStatusRepository):
        self.repository = repository
        self.jsonEncoder = JSONEncoder()

    def get(self, sinceTimestamp: float = None, untilTimestamp: float = None, limit: int = 100):
        if sinceTimestamp is not None and untilTimestamp is not None:
            return self.jsonEncoder.decode_to_dict(
                list(self.repository.get({"timestamp": {"$gt": sinceTimestamp, "$lt": untilTimestamp}}).limit(limit)))
        elif sinceTimestamp is not None:
            return self.jsonEncoder.decode_to_dict(
                list(self.repository.get({"timestamp": {"$gt": sinceTimestamp}}).limit(limit)))

        return self.jsonEncoder.decode_to_dict(list(self.repository.get({}).limit(100)))

    def __del__(self):
        self.mongoClient.close()


