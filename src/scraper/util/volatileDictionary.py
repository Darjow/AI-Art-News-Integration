import threading


class VolatileDict:
  def __init__(self):
    self._dict = {}
    self._lock = threading.Lock()
    self.index = 0

  def add_result(self, base_url, title):
    with self._lock:
      self._dict[self.index] = [base_url, title]
      self.index += 1
        
  def output_dict(self):
    url_dict = {}
    for key, value in self._dict.items():
      url = value[0] 
      if url in url_dict:
        url_dict[url].append(value[1]) 
      else:
        url_dict[url] = [value[1]] 
    return url_dict