from abc import abstractmethod


class TempChecker:

    @abstractmethod
    def get_temp(self):
        pass
