from parser import Parser
from GoogleBase import DataBase


class Wim:
    def __init__(self, trans_sheet_id):
        self.db = DataBase(trans_sheet_id)
        self.parser = Parser()
        pass

    def parseAndSaveToDataBase(self):
        transactions = self.parser.getTransaction('../op.xlsx')
        self.db.save_transactions(transactions)
        pass


if __name__ == "__main__":
    trans_sheet_id = "1ybWZLOwXOS4dAHWWL71-CKKhBWUHPKMbRKXjKfKDbC0"
    wim = Wim(trans_sheet_id)
    wim.parseAndSaveToDataBase()
    pass
