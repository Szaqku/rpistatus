from abc import abstractmethod


class TempStatusChecker:

    @abstractmethod
    def get_temp(self):
        pass
