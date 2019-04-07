import csv


class DataTable:
    PREDEFINED_HEADERS = None

    def is_headers_compatible(self, headers):
        if self.PREDEFINED_HEADERS is None or headers is None:
            return True
        missed_headers = set(self.PREDEFINED_HEADERS).difference(headers)
        return len(missed_headers) == 0

    def __init__(self, records=None, headers=None):
        if not self.is_headers_compatible(headers):
            raise AttributeError("Cannot find all required headers: "
                                 "headers must include {}".format(", ".join(self.PREDEFINED_HEADERS)))

        self.headers = headers or self.PREDEFINED_HEADERS
        self.header_index = {header: index for index, header in enumerate(self.headers)}

        self.records = records

    def load_csv(self, csv_file):
        csv_records = csv.reader(csv_file)
        headers = next(csv_records)
        self.__init__(csv_records, headers)
        return self

    def to_csv(self, filepath):
        with open(filepath, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.headers)
            writer.writerows(self.records)

    def dict_records(self):
        return map(lambda row: {
            self.headers[i]: row[i]
            for i in range(len(self.headers))
        }, self.records)

    def __iter__(self):
        return self.records


class OrderProductTable(DataTable):
    PREDEFINED_HEADERS = ["order_id", "product_id", "add_to_cart_order", "reordered"]

    def dict_records(self):
        return map(lambda row: {
            "product_id": row[1],
            "reordered": row[3] == '1'
        }, self.records)


class ProductTable(DataTable):
    PREDEFINED_HEADERS = ["product_id", "product_name", "aisle_id", "department_id"]


class DepartmentStaticsTable(DataTable):
    PREDEFINED_HEADERS = ["department_id", "number_of_orders", "number_of_first_orders", "percentage"]

    def __init__(self, records=None, departments=None):
        if not records and departments:
            records = {department_id: [department_id, 0, 0, 0] for department_id in departments}
        super().__init__(records)

    def add_order_count(self, department_id, count=1):
        self.records[department_id][1] += count

    def add_first_order_count(self, department_id, count=1):
        self.records[department_id][2] += count

    def summarize(self):
        if isinstance(self.records, dict):
            self.records = self.records.values()
        self.records = filter(lambda record: record[1] > 0, self.records)

        def calculate_ratio(row):
            row[3] = "{:.2f}".format(row[2] / row[1])
            return row
        self.records = map(calculate_ratio, self.records)

        self.records = sorted(self.records, key=lambda row: int(row[0]))
        return self.records



