from enum import Enum

from src.services.loggers.Logger import Logger
from src.services.loggers.LoggerFactory import LoggerFactory
from src.services.repositories.RepositoryFactory import RepositoryFactory
from src.services_impl.loggers.ConsoleLogger import ConsoleLogger
from src.services_impl.loggers.FileLogger import FileLogger
from src.services_impl.loggers.MongoDBLogger import MongoDBLogger


class Loggers(Enum):
    toFile: str = "file"
    toMongoDB: str = "mongodb"
    toConsole: str = "console"


class LoggerFactoryImpl(LoggerFactory):

    def __init__(self, configs, repositoryFactory: RepositoryFactory):
        self.repositoryFactory = repositoryFactory
        self.configs = configs

    def get_logger(self, name: str = None, loggerEnum: Loggers = None) -> Logger:
        if name is not None and \
                loggerEnum is not None and \
                name != loggerEnum.value:
            raise ValueError("Choose one logger by giving name OR loggerEnum")

        if name == Loggers.toFile.value or loggerEnum == Loggers.toFile:
            return FileLogger(self.repositoryFactory.get_repository("file"))
        elif name == Loggers.toMongoDB.value or loggerEnum == Loggers.toMongoDB:
            return MongoDBLogger(self.repositoryFactory.get_repository("mongodb"))
        elif name == Loggers.toConsole.value or loggerEnum == Loggers.toConsole:
            return ConsoleLogger()
        else:
            raise ValueError("Logger not found. Check function args")
