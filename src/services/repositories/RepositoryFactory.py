from abc import abstractmethod

from src.services.repositories.Respository import Repository


class RepositoryFactory:

    @abstractmethod
    def get_repository(self, name: str, configs) -> Repository:
        pass
