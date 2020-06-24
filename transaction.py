import hashlib
from datetime import datetime


class Transaction:
    def __init__(self, date: str, value, target, cat=-1, id=None):
        super().__init__()
        self.date = date
        self.value = value
        self.target = target
        self.cat = cat
        self.id = id or self._generate_id()

    def _generate_id(self):
        h = hashlib.new('ripemd160')
        h.update(F"{self}".encode())
        return h.hexdigest()[0:20]

    def toValueList(self):
        return [self.id, self.date, self.value, self.target, self.cat]

    def toDict(self):
        return {"id": self.id, "value": self.value, "date": self.date, "target": self.target, "cat": self.cat}

    def __repr__(self):
        return F"<Transaction {self.date} {self.value} {self.target}>"
