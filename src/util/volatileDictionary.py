import threading
import json


class VolatileDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.Lock()
        self.index = 0

    def add_result(self, base_url, title):
        with self._lock:
            self._dict[self.index] = [base_url, title]
            self.index += 1
            
            
    def get_dict(self):
        with self._lock:
            for key, value in self._dict.items():
                print(f"{value[0]} - {value[1]}")