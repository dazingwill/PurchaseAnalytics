import csv
from collections.abc import Iterable


class DataTable:
    """
    General table structure with lines and headers

    self.headers: a list of header str
    self.records: iterable object, elements type is list. Expected used only once.

    Usage:
    import data form csv file: table = DataTable.from_csv(csv_file)
    save this table to csv file: table.to_csv(filepath)
    iter records: for row in table
    iter records in dict format: for row in table.dict_records()
    """

    # if PREDEFINED_HEADERS is defined,
    # the headers in this table must include all the fields PREDEFINED_HEADERS have.
    PREDEFINED_HEADERS = None

    def __init__(self, records=None, headers=None):
        if not self.is_headers_compatible(headers):
            if self.PREDEFINED_HEADERS is None:
                raise TypeError("headers cannot be empty")
            else:
                raise ValueError("Cannot find all required headers: "
                                 "headers must include {}".format(", ".join(self.PREDEFINED_HEADERS)))
        if not isinstance(records, Iterable):
            raise TypeError("records must be iterable")

        self.headers = headers or self.PREDEFINED_HEADERS
        self.header_index = {header: index for index, header in enumerate(self.headers)}
        self.records = records

    def __iter__(self):
        return self.records

    @classmethod
    def from_csv(cls, csv_file):
        csv_records = csv.reader(csv_file)
        headers = next(csv_records)
        table = cls(csv_records, headers)
        return table

    def is_headers_compatible(self, headers):
        if self.PREDEFINED_HEADERS is None or headers is None:
            return self.PREDEFINED_HEADERS or headers
        missed_headers = set(self.PREDEFINED_HEADERS).difference(headers)
        return len(missed_headers) == 0

    def to_csv(self, filepath):
        with open(filepath, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.headers)
            writer.writerows(self.records)

    def dict_records(self):
        return map(lambda row: {
            self.headers[i]: row[i]
            for i in range(min(len(self.headers), len(row)))
        }, self.records)


class OrderProductTable(DataTable):
    """
    Table class for order records
    """
    PREDEFINED_HEADERS = ["order_id", "product_id", "add_to_cart_order", "reordered"]

    # Note: hardcoded this transfer function to make it faster
    def dict_records(self):
        product_id_index = self.header_index["product_id"]
        reordered_index = self.header_index["reordered"]
        return map(lambda row: {
            "product_id": row[product_id_index],
            "reordered": row[reordered_index] == '1'
        }, self.records)


class ProductTable(DataTable):
    """
    Table class for product records
    """
    PREDEFINED_HEADERS = ["product_id", "product_name", "aisle_id", "department_id"]

