import importlib
import sys

from flask import Flask

from src.main.StatusCheckerThread import StatusCheckerThread
from src.main.StatusRestApi import StatusRestApi
from src.services_impl.loggers.LoggerFactoryImpl import LoggerFactoryImpl
from src.services_impl.checkers.RpiCpuLoadStatusChecker import RpiCpuLoadStatusChecker
from src.services_impl.checkers.RpiMemoryStatusChecker import RpiMemoryStatusChecker
from src.services_impl.checkers.RpiNetworkStatusChecker import RpiNetworkStatusChecker
from src.services_impl.checkers.RpiTempStatusChecker import RpiTempStatusChecker
from src.services_impl.repositories.RepositoryFactoryImpl import RepositoryFactoryImpl

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

    repositoryFactory = RepositoryFactoryImpl(configs)
    loggerFactory = LoggerFactoryImpl(configs, repositoryFactory)

    data_collectors = [
        ("memory", RpiMemoryStatusChecker()),
        ("temperature", RpiTempStatusChecker()),
        ("cpu_load", RpiCpuLoadStatusChecker()),
        ("network", RpiNetworkStatusChecker())
    ]

    loggers = []
    for key, flag in app_config['loggers'].items():
        if flag:
            loggers.append(loggerFactory.get_logger(key))

    statusThread = StatusCheckerThread(tuple(loggers),
                                       data_collectors,
                                       app_config['loggingInterval'])

    statusThread.start()
    app = Flask(__name__)
    api = StatusRestApi(app, repositoryFactory.get_repository(app_config["main_data_source"]), statusThread)
    app.run(host=app_config['host'], port=app_config['port'])
