from abc import abstractmethod

from src.services.Logger import Logger


class LoggerFactory:

    @abstractmethod
    def get_logger(self, name: str) -> Logger:
        pass
