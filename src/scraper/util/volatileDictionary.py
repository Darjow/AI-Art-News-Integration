import threading


class VolatileDict:
  def __init__(self):
    self._dict = {}
    self._lock = threading.Lock()
    self.index = 0

  def add_result(self, title):
    with self._lock:
      self._dict[self.index] = title
      self.index += 1
        
  def output_dict(self):
    return self._dict.items()