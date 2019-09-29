import os

from src.services.TempStatusChecker import TempStatusChecker


class RpiTempStatusChecker(TempStatusChecker):
    def get_temp(self) -> dict:
        return (os.popen("vcgencmd measure_temp").read()).strip()