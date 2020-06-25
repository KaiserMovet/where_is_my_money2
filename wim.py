from .parser import Parser
from .googleBase import DataBase
from .transaction import Transaction


class Wim:
    def __init__(self, trans_sheet_id, semaphore=None):
        self.db = DataBase(trans_sheet_id, semaphore)
        self.parser = Parser()

    def parseAndSaveToDataBase(self, path):
        transactions = self.parser.getTransaction(path)
        self.db.save_transactions(transactions)

    def get_transactions(self, year="", month=""):
        res = self.db.get_transactions(year, month)
        trans_list = []
        for row in res:
            trans_obj = Transaction(
                date=row[1], value=row[2], target=row[3], cat=row[5], id=row[0])
            trans_list.append(trans_obj)
        return trans_list

    def edit_cat_of_transaction(self, trans_id: str, cat: int):
        self.db.edit_cat_of_transaction(trans_id, cat)

    def edit_cat_of_target(self, target: str, cat: int):
        self.db.edit_cat_of_target(target, cat)

    def get_cat(self):
        return self.db.get_cat()

    def get_cat_base(self):
        return self.db.get_cat_base()
