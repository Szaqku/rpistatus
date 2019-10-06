import flask_restful
from pymongo.collection import Collection

from src.main.StatusCheckerThread import StatusCheckerThread
from src.services.resources.Status import Status
from src.services.resources.Statuses import StatusList


class StatusRestApi(flask_restful.Api):
    collection: Collection

    def __init__(self, import_name, configs, statusThread: StatusCheckerThread):
        super().__init__(import_name)
        self.statusTread = statusThread
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
