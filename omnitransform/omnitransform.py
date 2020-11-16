import csv
import io
from tempfile import NamedTemporaryFile

from openpyxl import Workbook

from django.http import HttpResponse


class Transform:
    """
    input_dict = A list of dictionaries
    output_format = 'csv', 'xlsx'
    output_method = 'object' or 'response'
    """
    def __init__(self, input_dict):
        self.empty_value = ''
        self.filename = ''
        self.data = input_dict
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
                row.append(data_row.get(h, self.empty_value))
            body_rows.append(row)
        return body_rows

    def _generate_csv(self):
        """
        Returns a StringIO object
        Get the data using tmp.getvalue()
        """
        output_list = []
        output_list.append(self.headers)
        output_list += self.body
        tmp = io.StringIO()
        writer = csv.writer(tmp).writerows(output_list)
        tmp.seek(0)
        return tmp

    def _generate_xlsx(self):
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
        tmpfile = NamedTemporaryFile(mode='rb+')
        # with NamedTemporaryFile(mode='rb+') as tmpfile:
        wb.save(tmpfile.name)
        tmpfile.seek(0)
        tmp = io.BytesIO(tmpfile.read())
        tmpfile.close()
        return tmp

    def _response(self, obj, typeof):
        if typeof == 'csv':
            content_type = 'text/csv'
        elif typeof == 'xlsx':
            content_type = 'application/vnd.ms-excel'
        else:
            raise NotImplementedError(f"'{typeof}' is not implemented")

        resp = HttpResponse(obj, content_type=content_type)
        resp['Content-Disposition'] = f'attachment; filename="{self.filename}.{typeof}"'
        return resp


    # Public methods
    # XLSX
    def get_xlsx_response(self, filename, empty_value=''):
        self.filename = filename
        if empty_value:
            self.empty_value = empty_value
        obj = self._generate_xlsx()
        response = self._response(obj, typeof='xlsx')
        return response


    def get_xlsx_obj(self):
        return self._generate_xlsx()


    # CSV
    def get_csv_response(self, filename, empty_value=''):
        self.filename = filename
        if empty_value:
            self.empty_value = empty_value
        obj = self._generate_csv()
        response = self._response(obj, typeof='csv')
        return response


    def get_csv_obj(self):
        return self._generate_csv()


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
