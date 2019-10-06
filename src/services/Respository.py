from abc import abstractmethod


class Repository:

    @abstractmethod
    def get(self, filters: dict):
        pass

    @abstractmethod
    def create(self, data: dict):
        pass

    @abstractmethod
    def delete(self, filters: dict):
        pass
