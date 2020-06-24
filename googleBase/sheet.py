from .googleBase import GoogleBase

SAMPLE_RANGE_NAME = 'A2:E'


class Sheet:
    def __init__(self, sheet_id):
        self.service = GoogleBase().get_service()
        self.sheet_id = sheet_id

    def _get_results(self, sheet, range="A1:Z"):
        range_name = F"{sheet}!" + range
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id,
                                    range=range_name).execute()
        return result

    def get_data(self, sheet):
        result = self._get_results(sheet)
        return result["values"]

    def execute_query(self, query_sheet, query):
        query_command = F'=QUERY({query_sheet}!A1:Z;"SELECT * {query}")'
        self._write_data([[query_command]], "query", "A1")
        result = self.get_data("query")
        return result

    def _write_data(self, values: list, sheet, range="A1:Z"):
        body = {"values": values}
        range_name = F"{sheet}!" + range
        sheet = self.service.spreadsheets()
        sheet.values().update(spreadsheetId=self.sheet_id,
                              valueInputOption="USER_ENTERED",
                              range=range_name, body=body).execute()

    def write_data(self, values: list, sheet, range):
        self._write_data(values, sheet, range)

    def _append_data(self, values: list, sheet, range="A1:Z"):
        body = {"values": values}
        range_name = F"{sheet}!" + range
        sheet = self.service.spreadsheets()
        sheet.values().append(spreadsheetId=self.sheet_id,
                              valueInputOption="USER_ENTERED",
                              insertDataOption="INSERT_ROWS",
                              range=range_name, body=body).execute()

    def append_data(self, values: list, sheet, range="A1:Z"):
        self._append_data(values, sheet, range)

    def find(self, value, sheet, range="A:A"):
        value = F'=MATCH("{value}";{sheet}!{range};0)'
        self._write_data([[value]], "query", "A1")
        result = self.get_data("query")
        return result[0][0]
