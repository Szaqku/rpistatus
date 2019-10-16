from src.services.DataCollector import DataCollector


class DummyDataCollector(DataCollector):

    def __init__(self, data: any):
        self.data = data

    def get_data(self) -> dict:
        return self.data
