import json
import os
import re

from src.services.repositories.Respository import Repository


# TODO: Think about better solution

class FileStatusRepository(Repository):

    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    def get(self, filters: dict):
        # Works with timestamp filter only
        # since and until keys as filters for timestamp param
        return self.read_until(lambda x: int(re.search("\"timestamp\": (\\d+)", x)[1]) < filters['timestamp']['$gt'])

    def create(self, data: dict):
        self.save_record(data)

    def delete(self, filters: dict):
        # No need to implement this for now
        pass

    def save_record(self, record):
        with open(self.path_to_file, "a+") as file_handler:
            json.dump(record, file_handler)
            file_handler.write("\n")

    def read_until(self, until_condition):
        return [json.loads(record) for record in readlines_reverse(self.path_to_file, until_condition)]


def readlines_reverse(filename, condition):
    with open(filename) as qfile:
        qfile.seek(0, os.SEEK_END)
        position = qfile.tell()
        line = ''
        while position >= 0:
            qfile.seek(position)
            next_char = qfile.read(1)
            if next_char == "\n":
                if line != "":
                    if condition(line[::-1]):
                        return
                    yield line[::-1]
                line = ''
            else:
                line += next_char
            position -= 1
        yield line[::-1]
