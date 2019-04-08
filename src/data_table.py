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

    def is_headers_compatible(self, headers):
        if self.PREDEFINED_HEADERS is None or headers is None:
            return self.PREDEFINED_HEADERS or headers
        missed_headers = set(self.PREDEFINED_HEADERS).difference(headers)
        return len(missed_headers) == 0

    def __init__(self, records=None, headers=None):
        if not self.is_headers_compatible(headers):
            raise ValueError("Cannot find all required headers: "
                             "headers must include {}".format(", ".join(self.PREDEFINED_HEADERS)))
        if not isinstance(records, Iterable):
            raise TypeError("records must be iterable")

        self.headers = headers or self.PREDEFINED_HEADERS
        self.records = records

    @classmethod
    def from_csv(cls, csv_file):
        csv_records = csv.reader(csv_file)
        headers = next(csv_records)
        table = cls(csv_records, headers)
        return table

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

    def __iter__(self):
        return self.records


class OrderProductTable(DataTable):
    """
    Table class for order records
    """
    PREDEFINED_HEADERS = ["order_id", "product_id", "add_to_cart_order", "reordered"]

    # Note: hardcoded this transfer function to make it faster
    def dict_records(self):
        return map(lambda row: {
            "product_id": row[1],
            "reordered": row[3] == '1'
        }, self.records)


class ProductTable(DataTable):
    """
    Table class for product records
    """
    PREDEFINED_HEADERS = ["product_id", "product_name", "aisle_id", "department_id"]


class DepartmentStaticsTable(DataTable):
    """
    Table class for department statics

    to create a blank department statics table:
    table = DepartmentStaticsTable(departments=possible_department_ids)

    the records is usually in dict format, only calculate ratio and reorder before print to csv
    """
    PREDEFINED_HEADERS = ["department_id", "number_of_orders", "number_of_first_orders", "percentage"]

    def __init__(self, records=None, departments=None):
        if not records and departments is not None:
            records = {department_id: [department_id, 0, 0, 0] for department_id in departments}
        super().__init__(records)

    def add_order_count(self, department_id, count=1):
        self.records[department_id][1] += count

    def add_first_order_count(self, department_id, count=1):
        self.records[department_id][2] += count

    def summarize(self):
        if isinstance(self.records, dict):
            self.records = self.records.values()

        # remove the rows with no order count
        self.records = filter(lambda record: record[1] > 0, self.records)

        def calculate_ratio(row):
            row[3] = "{:.2f}".format(row[2] / row[1])
            return row
        self.records = map(calculate_ratio, self.records)

        # put rows in increasing order of department's id
        self.records = sorted(self.records, key=lambda row: int(row[0]))
        return self.records

    def to_csv(self, filepath):
        self.summarize()
        super().to_csv(filepath)
