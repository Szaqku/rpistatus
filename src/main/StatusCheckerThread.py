import importlib
import sys
import time
from datetime import datetime

from threading import Thread

from src.services.Logger import Logger
from src.services.MemoryStatusChecker import MemoryStatusChecker
from src.services.CpuLoadStatusChecker import CpuLoadStatusChecker
from src.services.NetworkStatusChecker import NetworkStatusChecker
from src.services.TempStatusChecker import TempStatusChecker
from src.services.impl.LoggerFactoryImpl import LoggerFactoryImpl
from src.services.impl.RpiCpuLoadStatusChecker import RpiCpuLoadStatusChecker
from src.services.impl.RpiMemoryStatusChecker import RpiMemoryStatusChecker
from src.services.impl.RpiNetworkStatusChecker import RpiNetworkStatusChecker
from src.services.impl.RpiTempStatusChecker import RpiTempStatusChecker


class StatusCheckerThread(Thread):
    logger: Logger
    tempChecker: TempStatusChecker
    memoryChecker: MemoryStatusChecker
    cpuLoadChecker: CpuLoadStatusChecker
    networkChecker: NetworkStatusChecker
    refreshInterval: int
    lastStatus: dict

    def __init__(self, logger: Logger,
                 memoryChecker: MemoryStatusChecker,
                 tempChecker: TempStatusChecker,
                 cpuLoadChecker: CpuLoadStatusChecker,
                 networkChecker: NetworkStatusChecker,
                 refreshInterval: int = 60):
        super().__init__()
        self.networkChecker = networkChecker
        self.cpuLoadChecker = cpuLoadChecker
        self.refreshInterval = refreshInterval
        self.tempChecker = tempChecker
        self.memoryChecker = memoryChecker
        self.logger = logger

    def run(self):
        while True:
            data = {}

            data["temperature"] = self.tempChecker.get_temp()

            data["memory"] = self.memoryChecker.get_mem_usage()

            data["cpu_load"] = self.cpuLoadChecker.get_avg_cpu_load()

            data["networks"] = self.networkChecker.get_network_status()

            data['timestamp'] = datetime.now().timestamp()

            self.logger.log(data)
            self.lastStatus = data

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

    with StatusCheckerThread(LoggerFactoryImpl(configs).get_logger(name=app_config['logger']),
                             RpiMemoryStatusChecker(),
                             RpiTempStatusChecker(),
                             RpiCpuLoadStatusChecker(),
                             RpiNetworkStatusChecker(),
                             app_config['loggingInterval']
                             ) as th:
        th.start()
