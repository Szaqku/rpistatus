from src.services.Logger import Logger


class DummyLogger(Logger):

    def log(self, data: any):
        print(data)