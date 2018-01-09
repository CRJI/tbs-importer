import json

class BaseWriter:

    def __init__(self, writable):
        self.writable = writable

    def dump(self):
        # return self.writable.to_json()
        return json.dumps(self.writable, ensure_ascii=False)
