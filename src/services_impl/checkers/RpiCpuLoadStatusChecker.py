import os
from re import split

from src.services.DataCollector import DataCollector


class RpiCpuLoadStatusChecker(DataCollector):

    def get_data(self) -> dict:
        avg_load = os.popen("cat /proc/loadavg").read().strip()
        nproc = int(os.popen("nproc").read().strip())

        cols = ['avg_1min', 'avg_5min', 'avg_10min']
        vals = split(r"\s|/", avg_load)

        data = dict(zip(cols, list(map(float, vals))))
        data['processing_units'] = nproc

        return data
