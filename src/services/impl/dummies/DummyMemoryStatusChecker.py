from src.services.MemoryStatusChecker import MemoryStatusChecker


class DummyMemoryStatusChecker(MemoryStatusChecker):
    def get_mem_usage(self):
        return {"mem": {"used": "2Gib"}}
