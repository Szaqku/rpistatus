import os

from src.services.DataCollector import DataCollector


class UptimeStatusChecker(DataCollector):
    def get_data(self) -> dict:
        uptime_output = os.popen("cat /proc/uptime").read().strip()
        uptime = uptime_output[0:uptime_output.index(".")]
        return {"time: ": int(uptime), "unit": "seconds"}
