import flask_restful

from src.main.StatusCheckerThread import StatusCheckerThread
from src.services.utlis.JSONEncoder import JSONEncoder


class Status(flask_restful.Resource):
    def __init__(self, statusChecker: StatusCheckerThread):
        self.statusChecker = statusChecker
        self.jsonEncoder = JSONEncoder()

    def get(self):
        return self.statusChecker.lastStatus
