import importlib
import sys

from flask import Flask

from src.main.StatusCheckerThread import StatusCheckerThread
from src.main.StatusRestApi import StatusRestApi
from src.services_impl.LoggerFactoryImpl import LoggerFactoryImpl
from src.services_impl.checkers.RpiCpuLoadStatusChecker import RpiCpuLoadStatusChecker
from src.services_impl.checkers.RpiMemoryStatusChecker import RpiMemoryStatusChecker
from src.services_impl.checkers.RpiNetworkStatusChecker import RpiNetworkStatusChecker
from src.services_impl.checkers.RpiTempStatusChecker import RpiTempStatusChecker

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

    data_collectors = [
        ("memory", RpiMemoryStatusChecker()),
        ("temperature", RpiTempStatusChecker()),
        ("cpu_load", RpiCpuLoadStatusChecker()),
        ("network", RpiNetworkStatusChecker())
    ]

    statusThread = StatusCheckerThread(LoggerFactoryImpl(configs).get_logger(app_config['logger']), app_config['loggingInterval']
                                       )

    statusThread.start()
    app = Flask(__name__)
    api = StatusRestApi(app, configs, statusThread)
    app.run(host=app_config['host'], port=app_config['port'])