import importlib
import sys

from flask import Flask
import flask_restful
from pymongo.collection import Collection

from src.main.StatusCheckerThread import StatusCheckerThread
from src.services.LoggerFactory import LoggerFactory
from src.services.impl.ConsoleLogger import ConsoleLogger
from src.services.impl.LoggerFactoryImpl import Loggers
from src.services.resources.Status import Status
from src.services.resources.Statuses import StatusList
from tests.dummies.DummyCpuLoadStatusChecker import DummyCpuLoadStatusChecker
from tests.dummies.DummyMemoryStatusChecker import DummyMemoryStatusChecker
from tests.dummies.DummyNetworkStatusChecker import DummyNetworkStatusChecker
from tests.dummies.DummyTempStatusChecker import DummyTempStatusChecker


class StatusRestApi(flask_restful.Api):
    collection: Collection

    def __init__(self, import_name, configs, statusTread: StatusCheckerThread):
        super().__init__(import_name)
        self.statusTread = statusTread
        self.configs = configs
        self.add_resource(Status, "/status/last",
                          resource_class_args=(statusThread,),
                          endpoint="lastStatus")
        self.add_resource(StatusList, "/status/",
                          resource_class_args=(configs,),
                          endpoint="fullStatusList")
        self.add_resource(StatusList, "/status/<int:sinceTimestamp>/<int:untilTimestamp>",
                          resource_class_args=(configs,),
                          endpoint="statusListBetweenDates")
        self.add_resource(StatusList, "/status/<int:sinceTimestamp>",
                          resource_class_args=(configs,),
                          endpoint="statusListSince")


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

    statusThread = StatusCheckerThread(ConsoleLogger(),
                                       DummyMemoryStatusChecker(),
                                       DummyTempStatusChecker(),
                                       DummyCpuLoadStatusChecker(),
                                       DummyNetworkStatusChecker(),
                                       10)

    statusThread.start()
    app = Flask(__name__)
    api = StatusRestApi(app, configs, statusThread)
    app.run(host=app_config['host'], port=app_config['port'])
