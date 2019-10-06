from abc import abstractmethod


class Logger:

    @abstractmethod
    def log(self, data: any):
        pass
