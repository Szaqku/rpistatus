import time
from datetime import datetime

from threading import Thread

from src.services.loggers.Logger import Logger


class StatusCheckerThread(Thread):

    def __init__(self, logger: Logger, data_collectors_map: list, refreshInterval: int = 60):
        super().__init__()
        self.lastStatus = None
        self.logger = logger
        self.data_collectors_map = data_collectors_map
        self.refreshInterval = refreshInterval

        self.setDaemon(True)

    def run(self):
        while True:
            data = {}

            for field_name, data in self.data_collectors_map:
                data[field_name] = data

            data['timestamp'] = datetime.now().timestamp()

            self.logger.log(data)

            time.sleep(self.refreshInterval)

    def get_last_status(self):
        return self.lastStatus

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return 0
