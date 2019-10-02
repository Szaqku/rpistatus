import importlib
import sys

from flask import Flask
import flask_restful
from pymongo import MongoClient
from pymongo.collection import Collection


class StatusRestApi(flask_restful.Api):
    collection: Collection

    class Status(flask_restful.Resource):
        def __init__(self, databaseName: str = "test", collectionName: str = "rpistatus"):
            self.mongoClient = MongoClient(configs['mongodb_config']['url'])
            self.collection = self.mongoClient[databaseName][collectionName]

        def get(self):
            return self.collection.find()

        def __del__(self):
            self.mongoClient.close()

    def __init__(self, import_name, configs):
        super().__init__(import_name)
        self.configs = configs
        self.add_resource(StatusRestApi, "/status/")


if __name__ == '__main__':
    import src.configs.config as configs

    if len(sys.argv) > 1:
        try:
            configs = importlib.import_module("src.configs." + sys.argv[1])
        except ModuleNotFoundError as ex:
            print("Couldn't load given config file with name: ", sys.argv[1])
            print(ex)

    mongodb_config = configs.mongodb_config
    app_config = configs.app_config
    print("Loaded config file: ", configs)

    app = Flask(__name__)
    api = StatusRestApi(__name__, configs)
    api.init_app(app)
