import importlib
import sys

from flask import Flask

from src.main.StatusCheckerThread import StatusCheckerThread
from src.main.StatusRestApi import StatusRestApi
from src.services_impl.checkers.RpiCpuLoadStatusChecker import RpiCpuLoadStatusChecker
from src.services_impl.checkers.RpiMemoryStatusChecker import RpiMemoryStatusChecker
from src.services_impl.checkers.RpiNetworkStatusChecker import RpiNetworkStatusChecker
from src.services_impl.checkers.RpiTempStatusChecker import RpiTempStatusChecker
from src.services_impl.loggers.ConsoleLogger import ConsoleLogger
from src.services_impl.loggers.FileLogger import FileLogger
from src.services_impl.loggers.MongoDBLogger import MongoDBLogger
from src.services_impl.repositories.MongoDBStatusRepository import MongoDBStatusRepository
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

    repository = RepositoryFactoryImpl().get_repository(app_config['repository'], configs)

    data_collectors = [
        ("memory", RpiMemoryStatusChecker()),
        ("temperature", RpiTempStatusChecker()),
        ("cpu_load", RpiCpuLoadStatusChecker()),
        ("network", RpiNetworkStatusChecker())
    ]

    loggers = []
    if app_config['loggers']['console']:
        loggers.append(ConsoleLogger())
    if app_config['loggers']['file']:
        loggers.append(FileLogger(configs.file_logger_config['path']))
    if app_config['loggers']['mongodb']:
        if not isinstance(repository, MongoDBStatusRepository):
            raise Exception("Change repository in configs to 'mongodb'")
        loggers.append(MongoDBLogger(repository))

    statusThread = StatusCheckerThread(tuple(loggers),
                                       data_collectors,
                                       app_config['loggingInterval'])

    statusThread.start()
    app = Flask(__name__)
    api = StatusRestApi(app, configs, statusThread)
    app.run(host=app_config['host'], port=app_config['port'])
