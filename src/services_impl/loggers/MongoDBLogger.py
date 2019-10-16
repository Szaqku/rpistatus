from src.services.loggers.Logger import Logger
from src.services_impl.repositories.MongoDBStatusRepository import MongoDBStatusRepository


class MongoDBLogger(Logger):

    def __init__(self, repository: MongoDBStatusRepository):
        self.repository = repository

    def log(self, data: dict):
        self.repository.create(data.copy())
