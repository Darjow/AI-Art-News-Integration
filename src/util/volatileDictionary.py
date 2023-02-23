import threading
import json

class VolatileDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.Lock()
        self.index = 0

    def add_result(self, base_url, article):
        with self._lock:
            params = {k: v for k, v in locals().items() if k!= "self"} #voor als de parameters die meegegeven wordt vergroten
            self._dict[self.index] = json.dumps(params) #{0: '{"base_url": "www.hln.be", "result": "https://www.hln.be/buitenland/vandaag-of-morgen-ze-hebben-twee-data-chef-oekraiense-inlichtingendienst-die-invasie-tot-op-uur-juist-voorspelde-verwacht-nu-alleen-raketaanval~a2dcf77f/"}'}
            self.index +=  1
            
            
    def get_dict(self):
        with self._lock:
            return self._dict