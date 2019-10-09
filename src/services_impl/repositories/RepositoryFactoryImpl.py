from pymongo import MongoClient

from src.services.repositories.RepositoryFactory import RepositoryFactory
from src.services.repositories.Respository import Repository
from src.services_impl.repositories.FileStatusRepository import FileStatusRepository
from src.services_impl.repositories.MongoDBStatusRepository import MongoDBStatusRepository


class RepositoryFactoryImpl(RepositoryFactory):

    def get_repository(self, name: str, configs) -> Repository:
        if name == "mongodb":
            return MongoDBStatusRepository(MongoClient(configs.mongodb_config['url']),
                                           configs.mongodb_config['database'],
                                           configs.mongodb_config['collection'])
        elif name == "file":
            return FileStatusRepository(configs.file_logger_config['path'])
        else:
            raise Exception("Repository not found. Check config file")