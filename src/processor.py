import csv
from collections import namedtuple


class TableProcessor:

    def _update_header_indexes(self):
        self.header_index = None
        if self.headers and self.records:
            self.header_index = {header: index for index, header in enumerate(self.headers)}
        return self.header_index

    def __init__(self, headers=None, records=None):
        self.headers = headers
        self.records = records
        self.header_index = self._update_header_indexes()

    def load_csv(self, csv_file):
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        self.records = csv_reader
        self.headers = headers
        self.header_index = self._update_header_indexes()
        return self

    def to_csv(self, filepath):
        with open(filepath, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.headers)
            writer.writerows(self.records)

    def __iter__(self):
        return self.records



class ProductDepartmentReader(TableProcessor):

    def __init__(self):
        super().__init__()
        self.row = namedtuple("ProductDepartmentRecord", ["product_id", "dept_id"])

    def __next__(self):
        for line in self.data_iter:
            product_id = int(line[self.header_index["product_id"]])
            dept_id = int(line[self.header_index["department_id"]])
            yield self.row(product_id=product_id, dept_id=dept_id)


class OrderProductReader(TableProcessor):

    def __init__(self):
        super().__init__()

    def load_csv(self, csv_file):
        super().load_csv(csv_file)
        self.product_id_index = self.header_index["product_id"]
        self.reordered_index = self.header_index["reordered"]
        return self

    def __iter__(self):
        return self

    def __next__(self):
        line = next(self.data_iter)
        line[self.product_id_index] = int(line[self.product_id_index])
        line[self.reordered_index] = line[self.reordered_index] == "1"
        return line
