import os

from src.services.TempStatusChecker import TempChecker


class RpiTempChecker(TempChecker):
    def get_temp(self) -> dict:
        return (os.popen("vcgencmd measure_temp").read()).strip()