from src.services.TempStatusChecker import TempStatusChecker


class DummyTempStatusChecker(TempStatusChecker):
    def get_temp(self):
        return {"degrees": "10", "unit": "C"}
