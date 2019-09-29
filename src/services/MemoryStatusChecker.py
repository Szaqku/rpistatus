from abc import abstractmethod


class MemoryStatusChecker:

    @abstractmethod
    def get_mem_usage(self):
        pass
