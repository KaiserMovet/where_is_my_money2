import hashlib
from datetime import datetime


class Transaction:
    def __init__(self, date: datetime, value, target, cat=-1):
        super().__init__()
        self.date = date
        self.value = value
        self.target = target
        self.cat = cat
        self.id = self._generate_id()

    def _generate_id(self):
        h = hashlib.new('ripemd160')
        h.update(F"{self}".encode())
        return h.hexdigest()[0:20]

    def toValueList(self):
        return [self.id, self.date, self.value, self.target, self.cat]

    def __repr__(self):
        return F"<Transaction {self.date} {self.value} {self.target}>"


if __name__ == "__main__":
    print(Transaction("12", 2, "fdgsdg").id)
    print(Transaction("sdfsdf", 2.5766, "dsafaf").id)
    print(Transaction("1dstewt", 255, "astrqeg").id)
    print(Transaction("sdfvs", 2.8, "afaqg").id)
