import importlib
import sys
import time
from pymongo import MongoClient
from threading import Thread

from src.services.Logger import Logger
from src.services.MemoryStatusChecker import MemoryStatusChecker
from src.services.CpuLoadStatusChecker import CpuLoadStatusChecker
from src.services.TempStatusChecker import TempStatusChecker
from src.services.impl.MongoDBLogger import MongoDBLogger
from src.services.impl.RpiCpuLoadStatusChecker import RpiCpuLoadStatusChecker
from src.services.impl.RpiMemoryStatusChecker import RpiMemoryStatusChecker
from src.services.impl.RpiTempStatusChecker import RpiTempStatusChecker


class StatusCheckerThread(Thread):
    logger: Logger
    tempChecker: TempStatusChecker
    memoryChecker: MemoryStatusChecker
    cpuLoadChecker: CpuLoadStatusChecker
    refreshInterval: int

    def __init__(self, logger: Logger,
                 memoryChecker: MemoryStatusChecker,
                 tempChecker: TempStatusChecker,
                 cpuLoadChecker: CpuLoadStatusChecker,
                 refreshInterval: int = 60):
        super().__init__()
        self.cpuLoadChecker = cpuLoadChecker
        self.refreshInterval = refreshInterval
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

            cpu_load = self.cpuLoadChecker.get_avg_cpu_load()
            data["cpu_load"] = cpu_load

            self.logger.log(data)

            time.sleep(self.refreshInterval)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return 0


if __name__ == "__main__":
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

    with StatusCheckerThread(MongoDBLogger(MongoClient(mongodb_config['url'])),
                             RpiMemoryStatusChecker(),
                             RpiTempStatusChecker(),
                             RpiCpuLoadStatusChecker(),
                             app_config['loggingInterval']
                             ) as th:
        th.start()
