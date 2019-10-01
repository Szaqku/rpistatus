from enum import Enum

from pymongo import MongoClient

from src.services.Logger import Logger
from src.services.LoggerFactory import LoggerFactory
from src.services.impl.FileLogger import FileLogger
from src.services.impl.MongoDBLogger import MongoDBLogger


class Loggers(Enum):
    toFile: str = "FileLogger"
    toMongoDB: str = "MongoDBLogger"


class LoggerFactoryImpl(LoggerFactory):

    def __init__(self, configs):
        self.configs = configs

    def get_logger(self, name: str = None, loggerEnum: Loggers = None) -> Logger:
        if name is not None and \
                loggerEnum is not None and \
                name != loggerEnum.value:
            raise ValueError("Choose one logger by giving name OR loggerEnum")

        if name == Loggers.toFile.value or loggerEnum == Loggers.toFile:
            return FileLogger()
        elif name == Loggers.toMongoDB.value or loggerEnum == Loggers.toMongoDB:
            return MongoDBLogger(MongoClient(self.configs.mongodb_config['url']))
        else:
            raise ValueError("Logger not found. Check function args")
