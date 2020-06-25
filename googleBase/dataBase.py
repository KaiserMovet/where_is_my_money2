from contextlib import contextmanager
import threading
from .sheet import Sheet


class DataBase:
    DATA = "data"
    CAT = "cat"
    CAT_BASE = "cat_base"

    def __init__(self, sheet_id, semaphore=None):
        if semaphore is None:
            semaphore = threading.Semaphore()
        self._sem = semaphore
        self._sheet = Sheet(sheet_id)

    @contextmanager
    def _sheet_obj(self):
        self._sem.acquire()
        yield self._sheet
        self._sem.release()

    def save_transactions(self, transactions: list):
        id_query = " OR ".join(
            [F"A='{t.id}'" for t in transactions])
        with self._sheet_obj() as sheet:
            res = sheet.execute_query(self.DATA, F"WHERE {id_query}")
            current_ids = [row[0] for row in res]
            function_str = \
                "=IF(EQ(INDIRECT(ADDRESS(ROW();COLUMN()-1)); -1); "\
                "IF(ISNUMBER(VLOOKUP(INDIRECT(ADDRESS(ROW();COLUMN()-2));"\
                "cat_base!A:B;2; FALSE)); "\
                "VLOOKUP(INDIRECT(ADDRESS(ROW();COLUMN()-2));"\
                "cat_base!A:B;2; FALSE); 0);"\
                "INDIRECT(ADDRESS(ROW();COLUMN()-1)))"
            filtered_transactions = filter(
                lambda trans: trans.id not in current_ids, transactions)
            values = [trans.toValueList() for trans in filtered_transactions]
            [trans.append(function_str) for trans in values]

            sheet.append_data(values, self.DATA)

    def get_transactions(self, year=None, month=1):
        query = ""
        if year:
            if month and month < 12:
                next_year = year
                next_month = month + 1
            else:
                next_year = year + 1
                next_month = 1
            query = F"WHERE B>=date'{year}-{month}-1' AND B<date'{next_year}-{next_month}-1'"
        with self._sheet_obj() as sheet:
            res = sheet.execute_query(self.DATA, query)
        return res

    def edit_cat_of_transaction(self, trans_id: str, cat: int):
        with self._sheet_obj() as sheet:
            row_num = sheet.find(trans_id, self.DATA)
            cell_addr = F"E{row_num}"
            sheet.write_data([[cat]], self.DATA, cell_addr)

    def edit_cat_of_target(self, target: str, cat: int):
        with self._sheet_obj() as sheet:
            row_num = sheet.find(target, self.CAT_BASE)
            cell_addr = F"B{row_num}"
            sheet.write_data([[cat]], self.CAT_BASE, cell_addr)

    def get_cat(self):
        with self._sheet_obj() as sheet:
            res = sheet.get_data(self.CAT)
        res_dict = {}
        for row in res:
            res_dict[row[0]] = row[1]
        return res_dict

    def get_cat_base(self):
        with self._sheet_obj() as sheet:
            res = sheet.get_data(self.CAT_BASE)
        res_dict = []
        for row in res:
            if len(row) > 1:
                cat = row[1]
            else:
                cat = 0
            res_dict.append({"target": row[0], "cat": int(cat)})
        return res_dict
