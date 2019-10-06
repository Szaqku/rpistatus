from typing import TextIO

from src.services.loggers.Logger import Logger


class FileLogger(Logger):
    fileHandler: TextIO

    def __init__(self, fileName):
        self.fileHandler = open(fileName, "a+")

    def log(self, data: any):
        self.fileHandler.write(str(data)+"\n")
        self.fileHandler.flush()

    def __del__(self):
        self.fileHandler.close()
