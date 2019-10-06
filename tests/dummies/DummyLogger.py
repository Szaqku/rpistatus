from src.services.loggers.Logger import Logger


class DummyLogger(Logger):

    def log(self, data: any):
        print(data)