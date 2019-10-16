from pymongo import MongoClient

from src.services.repositories.RepositoryFactory import RepositoryFactory
from src.services.repositories.Respository import Repository
from src.services_impl.repositories.FileStatusRepository import FileStatusRepository
from src.services_impl.repositories.MongoDBStatusRepository import MongoDBStatusRepository


class RepositoryFactoryImpl(RepositoryFactory):

    def __init__(self, configs):
        self.mongodb = None
        self.file = None
        self.configs = configs

    def get_repository(self, name: str) -> Repository:
        if name == "mongodb":
            if self.mongodb is None:
                self.mongodb = MongoDBStatusRepository(MongoClient(self.configs.mongodb_config['url']),
                                                       self.configs.mongodb_config['database'],
                                                       self.configs.mongodb_config['collection'])
            return self.mongodb

        elif name == "file":
            if self.file is None:
                self.file = FileStatusRepository(self.configs.file_logger_config['path'])
            return self.file

        else:
            raise Exception("Repository not found. Check config file")
