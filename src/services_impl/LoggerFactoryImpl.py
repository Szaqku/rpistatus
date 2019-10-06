from enum import Enum

from pymongo import MongoClient

from src.services.loggers.Logger import Logger
from src.services.loggers.LoggerFactory import LoggerFactory
from src.impl.services.loggers.ConsoleLogger import ConsoleLogger
from src.impl.services.loggers.FileLogger import FileLogger
from src.impl.services.loggers.MongoDBLogger import MongoDBLogger


class Loggers(Enum):
    toFile: str = "FileLogger"
    toMongoDB: str = "MongoDBLogger"
    toConsole: str = "ConsoleLogger"


class LoggerFactoryImpl(LoggerFactory):

    def __init__(self, configs):
        self.configs = configs

    def get_logger(self, name: str = None, loggerEnum: Loggers = None) -> Logger:
        if name is not None and \
                loggerEnum is not None and \
                name != loggerEnum.value:
            raise ValueError("Choose one logger by giving name OR loggerEnum")

        if name == Loggers.toFile.value or loggerEnum == Loggers.toFile:
            return FileLogger(self.configs.file_config['path'])
        elif name == Loggers.toMongoDB.value or loggerEnum == Loggers.toMongoDB:
            return MongoDBLogger(MongoClient(self.configs.mongodb_config['url']))
        elif name == Loggers.toConsole.value or loggerEnum == Loggers.toConsole:
            return ConsoleLogger()
        else:
            raise ValueError("Logger not found. Check function args")
