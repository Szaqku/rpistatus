from abc import abstractmethod


class NetworkStatusChecker:

    @abstractmethod
    def get_network_status(self) -> dict:
        pass