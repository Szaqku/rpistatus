from src.services.loggers.Logger import Logger


class ConsoleLogger(Logger):

    def log(self, data: any):
        print(data)