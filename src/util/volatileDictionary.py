import threading

class VolatileDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.Lock()

    def add_result(self, thread_name, result):
        with self._lock:
            self._dict[thread_name] = result

    def get_dict(self):
        with self._lock:
            return self._dict