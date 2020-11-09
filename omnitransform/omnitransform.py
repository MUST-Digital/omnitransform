import csv
import io
from tempfile import NamedTemporaryFile

from openpyxl import Workbook


class Transform:
    """
    input_dict = A list of dictionaries
    output_format = 'csv', 'xlsx'
    output_method = 'object' or 'response'
    """
    def __init__(self, input_dict, output_format, output_method):
        self.data = input_dict
        self.output_format = output_format
        self.output_method = output_method
        self.headers = self._create_headers()
        self.body = self._create_body(self.headers)

    def _create_headers(self):
        headers = [k for k, v in {k:v for x in self.data for k, v in x.items()}.items()]
        return headers

    def _create_body(self, headers):
        body_rows = []
        for data_row in self.data:
            row = []
            for h in headers:
                row.append(data_row.get(h, ''))
            body_rows.append(row)
        return body_rows

    def _output_csv(self):
        """
        Returns a StringIO object
        Get the data using tmp.getvalue()
        """
        output_list = []
        output_list.append(self.headers)
        output_list += self.body
        tmp = io.StringIO()
        writer = csv.writer(tmp).writerows(output_list)
        return tmp

    def _output_xlsx(self):
        """
        Returns a NamedTemporaryFile object
        Get the data using tmp.getvalue()
        """
        wb = Workbook()
        ws = wb.active
        data = self.data
        ws.append(self.headers)
        for row in self.body:
            ws.append(row)
        with NamedTemporaryFile(mode='rb+') as tmpfile:
            wb.save(tmpfile.name)
            tmpfile.seek(0)
            return tmpfile

    def output(self):
        if self.output_format == 'csv':
            return self._output_csv()
        elif self.output_format == 'xlsx':
            return self._output_xlsx()
        else:
            raise NotImplementedError(f"output format {self.output_format} is not supported.")

    def output_format_file(self):
        pass


    def export_data(self, typeof):
        """
        data = [
            {'k1': 1, 'k2': 2, 'k3': 3},
            {'k1': 4, 'k2': 5, 'k3': 6}
        ]
        """
        data = self.data
        # Get headers, merge all keys
        headers = self.create_headers()

        if typeof == 'xlsx':
            wb = Workbook()
            ws = wb.active
            ws.append(headers)
            # Create a list of value lists
            data_list = []
            for data_row in data:
                row = []
                for h in headers:
                    row.append(data_row.get(h, ''))

                ws.append(row)
            with NamedTemporaryFile(mode='rb+') as tmpfile:
                wb.save(tmpfile.name)
                tmpfile.seek(0)
                return tmpfile.read()

        elif typeof == 'csv':
            tmpfile = io.StringIO()
            writer = csv.DictWriter(tmpfile, fieldnames=headers)
            writer.writeheader()
            for data_row in data:
                row = {}
                for h in headers:
                    row[h] = data_row.get(h, '')
                writer.writerow(row)
            tmpfile.seek(0)
            return tmpfile
        else:
            pass
        return
