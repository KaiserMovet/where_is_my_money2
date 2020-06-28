from contextlib import contextmanager
from .googleBase import GoogleBase

SAMPLE_RANGE_NAME = 'A2:E'


class Sheet:

    def __init__(self, sheet_id):
        self.service = GoogleBase().get_service()
        self.sheet_id = sheet_id

    @contextmanager
    def _sheet_values(self):
        yield self.service.spreadsheets().values()

    def _get_results(self, sheet, range="A1:F"):
        range_name = F"{sheet}!" + range
        with self._sheet_values() as sv:
            result = sv.get(spreadsheetId=self.sheet_id,
                            range=range_name).execute()
        return result

    def get_data(self, sheet):
        result = self._get_results(sheet)
        return result["values"]

    def execute_query(self, query_sheet_name, target_sheet, query="", columns="*"):
        print(F"SHEET NAME: {query_sheet_name}")
        query_command = F'=QUERY({target_sheet}!A1:Z;"SELECT {columns} {query}")'
        self._write_data([[query_command]], query_sheet_name, "A1")
        result = self.get_data(query_sheet_name)
        return result

    def _write_data(self, values: list, sheet, range="A1:F"):
        body = {"values": values}
        range_name = F"{sheet}!" + range
        with self._sheet_values() as sv:
            sv.update(spreadsheetId=self.sheet_id,
                      valueInputOption="USER_ENTERED",
                      range=range_name, body=body).execute()

    def write_data(self, values: list, sheet, range):
        self._write_data(values, sheet, range)

    def _append_data(self, values: list, sheet, range="A1:F"):
        body = {"values": values}
        range_name = F"{sheet}!" + range
        with self._sheet_values() as sv:
            sv.append(spreadsheetId=self.sheet_id,
                      valueInputOption="USER_ENTERED",
                      insertDataOption="INSERT_ROWS",
                      range=range_name, body=body).execute()

    def append_data(self, values: list, sheet, range="A1:F"):
        self._append_data(values, sheet, range)

    def find(self, value, sheet, range="A:A"):
        value = F'=MATCH("{value}";{sheet}!{range};0)'
        self._write_data([[value]], "query", "A1")
        result = self.get_data("query")
        return result[0][0]
