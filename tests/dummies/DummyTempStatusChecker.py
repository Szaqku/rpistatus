from src.services.TempStatusChecker import TempStatusChecker


class DummyTempStatusChecker(TempStatusChecker):
    def get_temp(self):
        return "10'C"
