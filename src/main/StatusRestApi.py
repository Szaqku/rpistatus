import importlib
import sys

import flask_restful
from flask import Flask
from pymongo.collection import Collection

from src.main.StatusCheckerThread import StatusCheckerThread
from src.services.impl.LoggerFactoryImpl import LoggerFactoryImpl
from src.services.impl.RpiCpuLoadStatusChecker import RpiCpuLoadStatusChecker
from src.services.impl.RpiMemoryStatusChecker import RpiMemoryStatusChecker
from src.services.impl.RpiNetworkStatusChecker import RpiNetworkStatusChecker
from src.services.impl.RpiTempStatusChecker import RpiTempStatusChecker
from src.services.resources.Status import Status
from src.services.resources.Statuses import StatusList


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

    statusThread = StatusCheckerThread(LoggerFactoryImpl(configs).get_logger(name=app_config['logger']),
                                       RpiMemoryStatusChecker(),
                                       RpiTempStatusChecker(),
                                       RpiCpuLoadStatusChecker(),
                                       RpiNetworkStatusChecker(),
                                       app_config['loggingInterval']
                                       )

    statusThread.start()
    app = Flask(__name__)
    api = StatusRestApi(app, configs, statusThread)
    app.run(host=app_config['host'], port=app_config['port'])
