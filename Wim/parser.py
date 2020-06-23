import pandas as pd
from pprint import pprint
from transaction import Transaction
VALUE = 3
DATE = 1
DESC = 6
SENDER = 5
TYPE = 8

decode_dict = {"\u0105": "a",
               "\u0107": "c",
               "\u0119": "e",
               "\u0142": "l",
               "\u0144": "n",
               "\u01F3": "o",
               "\u015B": "s",
               "\u017A": "z",
               "\u017C": "z",
               "\u0104": "A",
               "\u0106": "C",
               "\u0118": "E",
               "\u0141": "L",
               "\u0143": "N",
               "\u00D3": "O",
               "\u015A": "S",
               "\u0179": "Z",
               "\u017B": "Z"}


def desc_decode(desc: str):
    for key, value in decode_dict.items():
        desc = desc.replace(key, value)
    return desc


class Parser:
    def __init__(self):
        pass

    @classmethod
    def _get_target(cls, row):
        type_of_trans = desc_decode(row.iloc[TYPE])
        target = "unknown"
        if(type_of_trans in ['Przelew wychodzacy', 'Przelew przychodzacy', 'Zlecenie stale']):
            target = row.iloc[SENDER].splitlines()[1]
        elif(type_of_trans in ['Transakcja karta']):
            target = " ".join(row.iloc[DESC].split()[3: -4])
        elif(type_of_trans in ['Transakcja BLIK']):
            target = row.iloc[DESC].split(",")[2]

        return target.strip()

    @classmethod
    def _parse_row(cls, row, trans_list):
        target = cls._get_target(row)
        value = float(row.iloc[VALUE])
        date = row.iloc[DATE].to_pydatetime().strftime("%Y-%m-%d")
        trans = Transaction(date, value, target)
        trans_list.append(trans)

    @classmethod
    def getTransaction(cls, xls_file):
        xls = pd.ExcelFile(xls_file)
        sheetX = xls.parse(0)
        trans_list = []
        sheetX.apply(cls._parse_row, axis=1, trans_list=trans_list)
        # pprint(type(sheetX))
        return trans_list


if __name__ == "__main__":
    Parser.getTransaction("../op.xlsx")
