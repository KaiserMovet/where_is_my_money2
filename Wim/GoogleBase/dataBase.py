from .sheet import Sheet


class DataBase:
    DATA = "data"
    CAT = "cat"
    CAT_BASE = "cat_base"

    def __init__(self, sheet_id):
        self._sheet = Sheet(sheet_id)

    def save_transactions(self, transactions: list):
        id_query = " OR ".join(
            [F"A='{t.id}'" for t in transactions])
        res = self._sheet.execute_query(self.DATA, F"WHERE {id_query}")
        current_ids = [row[0] for row in res]
        function_str = "=IF(EQ(INDIRECT(ADDRESS(ROW();COLUMN()-1)); -1); IFERROR(VLOOKUP(INDIRECT(ADDRESS(ROW();COLUMN()-2));cat_base!A:B;2; FALSE); 0);INDIRECT(ADDRESS(ROW();COLUMN()-1)))"
        filtered_transactions = filter(
            lambda trans: trans.id not in current_ids, transactions)
        values = [trans.toValueList() for trans in filtered_transactions]
        [trans.append(function_str) for trans in values]
        self._sheet.append_data(values, self.DATA)

    def edit_cat_of_transaction():
        pass


if __name__ == "__main__":
    trans_sheet_id = "1ybWZLOwXOS4dAHWWL71-CKKhBWUHPKMbRKXjKfKDbC0"
    db = DataBase(trans_sheet_id)
    db.save_transactions([])
