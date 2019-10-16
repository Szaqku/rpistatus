import os

from src.services.DataCollector import DataCollector


class UpdateStatusChecker(DataCollector):

    def get_data(self) -> dict:
        upgradeable = os.popen("apt-get dist-upgrade -s --quiet=2 | grep ^Inst | wc -l").read().strip()
        return {"upgradeable: ": int(upgradeable)}