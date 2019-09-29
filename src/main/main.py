import importlib
import sys
import time
from pymongo import MongoClient
from threading import Thread

from src.services import Logger, MemoryStatusChecker
from src.services.TempStatusChecker import TempStatusChecker
from src.services.impl.MongoDBLogger import MongoDBLogger
from src.services.impl.RpiMemoryStatusChecker import RpiMemoryStatusChecker
from src.services.impl.RpiTempStatusChecker import RpiTempStatusChecker

from src.configs.config import mongodb_config
from src.configs.config import app_config

if len(sys.argv) > 0 and sys.argv[-1] == "dev":
    configs = importlib.import_module("src.configs._config")
    mongodb_config = configs.mongodb_config
    app_config = configs.app_config


class StatusCheckerThread(Thread):
    logger: Logger
    tempChecker: TempStatusChecker
    memoryChecker: MemoryStatusChecker

    def __init__(self, logger: Logger,
                 memoryChecker: MemoryStatusChecker,
                 tempChecker: TempStatusChecker):
        super().__init__()
        self.tempChecker = tempChecker
        self.memoryChecker = memoryChecker
        self.logger = logger

    def run(self):
        while True:
            data = {}

            temp = self.tempChecker.get_temp()
            data["temperature"] = temp

            memory = self.memoryChecker.get_mem_usage()
            data["memory"] = memory

            self.logger.log(data)
            time.sleep(app_config['loggingInterval'])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return 0


if __name__ == "__main__":
    with StatusCheckerThread(MongoDBLogger(MongoClient(mongodb_config['url'])),
                             RpiMemoryStatusChecker(),
                             RpiTempStatusChecker()) as th:
        th.start()
