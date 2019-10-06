from abc import abstractmethod

from src.services.loggers.Logger import Logger


class LoggerFactory:

    @abstractmethod
    def get_logger(self, name: str) -> Logger:
        pass
