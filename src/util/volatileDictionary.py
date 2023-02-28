import threading
import json


class VolatileDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.Lock()
        self.index = 0

    def add_result(self,title):
        with self._lock:
            self._dict[self.index] = title
            self.index += 1
            
            
    def get_dict(self):
        with self._lock:
            return self._dict