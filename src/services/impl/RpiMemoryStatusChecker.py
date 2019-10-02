import os
import re

from src.services.MemoryStatusChecker import MemoryStatusChecker


class RpiMemoryStatusChecker(MemoryStatusChecker):

    def get_mem_usage(self) -> dict:
        def create_dict_from_row(_cols: list, _values: list, _data: dict) -> None:
            _data[_values[0]] = {}
            for _x, _y in zip(_cols, map(int, _values[1:])):
                _data[_values[0]][_x] = _y

        data = {}
        pattern = r"([\w./]+)"
        output = (os.popen("free -m").read()).strip()

        strings = output.split("\n")
        cols = re.findall(pattern, strings[0])

        for i in (1, 2):
            create_dict_from_row(cols, re.findall(pattern, strings[i]), data)

        return data
