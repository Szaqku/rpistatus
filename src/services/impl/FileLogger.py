from typing import TextIO

from src.services.Logger import Logger


class FileLogger(Logger):
    fileHandler: TextIO

    def __init__(self, configs, filePath=None):
        self.fileHandler = open(filePath if filePath is not None else configs.file_config['path'], "a+")

    def log(self, data: any):
        self.fileHandler.write(str(data)+"\n")
        self.fileHandler.flush()

    def __del__(self):
        self.fileHandler.close()
