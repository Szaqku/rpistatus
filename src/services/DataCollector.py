from abc import abstractmethod


class DataCollector:

    @abstractmethod
    def get_data(self) -> dict:
        pass
