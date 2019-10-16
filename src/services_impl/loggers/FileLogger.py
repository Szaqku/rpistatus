from typing import TextIO

from src.services.loggers.Logger import Logger
from src.services_impl.repositories.FileStatusRepository import FileStatusRepository


class FileLogger(Logger):

    def __init__(self, repository: FileStatusRepository):
        self.repository = repository

    def log(self, data: any):
        self.repository.create(data)
