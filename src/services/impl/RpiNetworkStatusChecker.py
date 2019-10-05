import json
import os

from src.services.NetworkStatusChecker import NetworkStatusChecker


class RpiNetworkStatusChecker(NetworkStatusChecker):

    def get_network_status(self) -> dict:
        return json.loads(os.popen("ip -s -j addr show").read().strip())