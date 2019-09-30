from abc import abstractmethod


class CpuLoadStatusChecker:

    @abstractmethod
    def get_avg_cpu_load(self):
        pass
