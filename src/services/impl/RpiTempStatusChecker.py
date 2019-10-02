import os
import re

from src.services.TempStatusChecker import TempStatusChecker


class RpiTempStatusChecker(TempStatusChecker):

    def get_temp(self) -> dict:
        output = os.popen("vcgencmd measure_temp").read().strip()
        result = re.search(r"^(?:temp=)(\d+(?:\.\d|.*)+)'(.+)$", output)
        return {"degrees": result.group(1), "unit": result.group(2)}
