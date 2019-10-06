import json
import os

from src.services.DataCollector import DataCollector


class RpiNetworkStatusChecker(DataCollector):

    def get_data(self) -> dict:
        return json.loads(os.popen("ip -s -j addr show").read().strip())