from typing import TextIO

from src.services.Logger import Logger


class FileLogger(Logger):
    fileHandler: TextIO

    def __init__(self, fileName="logs.csv"):
        self.fileHandler = open(fileName, "a+")

    def log(self, data: any):
        self.fileHandler.write(data)
        self.fileHandler.flush()

    def __del__(self):
        self.fileHandler.close()
