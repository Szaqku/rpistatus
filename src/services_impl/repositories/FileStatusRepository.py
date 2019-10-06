import json

from src.services.Respository import Repository


def remove_if(function, elements):
    for el in elements:
        if function(el):
            del el


class FileStatusRepository(Repository):

    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    def get(self, filters: dict):
        # Works with timestamp filter only
        # since and until keys as filters for timestamp param

        if "since" in filters.keys() and "until" in filters.keys():
            return self.perform_operation_on_file(lambda data:
                                                  list(
                                                      filter(
                                                          lambda el:
                                                          el['timestamp'] >= filters["since"]
                                                          and el["timestamp"] < filters["until"], data)
                                                  ), "r+")
        elif "since" in filters.keys():
            return self.perform_operation_on_file(lambda data:
                                                  list(
                                                      filter(
                                                          lambda el: el['timestamp'] >= filters["since"], data)
                                                  ), "r+")

    def create(self, data: dict):
        self.perform_operation_on_file(lambda records: records.insert(0, data), "w+")

    def delete(self, filters: dict):
        # Works with timestamp filter only
        # since and until keys as filters for timestamp param

        if "since" in filters.keys() and "until" in filters.keys():
            return self.perform_operation_on_file(lambda data:
                                                  remove_if(
                                                          lambda el:
                                                          el['timestamp'] >= filters["since"]
                                                          and el["timestamp"] < filters["until"], data)
                                                  , "r+")
        elif "since" in filters.keys():
            return self.perform_operation_on_file(lambda data:
                                                  remove_if(
                                                      lambda el: el['timestamp'] >= filters["since"], data)
                                                  , "r+")

    def perform_operation_on_file(self, operation, file_mode):
        file_handler = open(self.path_to_file, file_mode)
        records = json.load(file_handler)

        response = operation(records)

        file_handler.truncate()
        json.dump(records, file_handler)

        return response
