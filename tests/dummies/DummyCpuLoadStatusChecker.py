from src.services.checkers.CpuLoadStatusChecker import CpuLoadStatusChecker


class DummyCpuLoadStatusChecker(CpuLoadStatusChecker):

    def get_avg_cpu_load(self) -> dict:
        return {'avg_1min': 0.00, 'avg_5min': 0.0, 'avg_10min': 0.0, 'processing_units': 1}