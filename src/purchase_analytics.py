import sys
import os

from data_table import DataTable, OrderProductTable, ProductTable


class DepartmentOrderCounter:
    """
    class for counting department orders.
    """
    def __init__(self, departments=None):
        """
        Init counter to count the department orders
        :param departments: iterable, contains all the possible department id.
        """
        self.counts = {
            department_id: {
                "department_id": department_id,
                "number_of_orders": 0,
                "number_of_first_orders": 0
            } for department_id in departments}

    def add_order_count(self, department_id, count=1):
        self.counts[department_id]["number_of_orders"] += count

    def add_first_order_count(self, department_id, count=1):
        self.counts[department_id]["number_of_first_orders"] += count

    def to_data_table(self):
        headers = ["department_id", "number_of_orders", "number_of_first_orders", "percentage"]
        records = self.counts.values()

        # remove the rows with no order count
        records = filter(lambda record: record["number_of_orders"] > 0, records)

        def calculate_ratio(record):
            row = [record["department_id"], record["number_of_orders"], record["number_of_first_orders"], 0]
            row[3] = "{:.2f}".format(row[2] / row[1])
            return row
        records = map(calculate_ratio, records)

        # put rows in increasing order of department's id
        records = sorted(records, key=lambda row: int(row[0]))
        return DataTable(records, headers)


def extract_product_departments(products_path):
    """
    Extract products' department id from csv file

    :param products_path: str, path of the csv file holds product records
    :return: product_departments: dict, map product id to department id
    """
    with open(products_path, "r", encoding="utf-8") as products_file:
        product_records = ProductTable.from_csv(products_file)

        product_departments = {row["product_id"]: row["department_id"] for row in product_records.dict_records()}
        return product_departments


def count_department_orders(order_products_path, product_departments):
    """
    For each departmentCount, count the orders and first orders made for the products in this department
    and save the numbers in a table.

    :param order_products_path: str, path of the csv file holds order records
    :param product_departments: dict, map product id to department id
    :return: department_statics: DepartmentOrderCounter, save the counts of orders for each department
    """

    # init department statics table
    departments = set(product_departments.values())
    department_statics = DepartmentOrderCounter(departments)

    # iterate order records from csv file and add counts into statics table
    with open(order_products_path, "r", encoding="utf-8") as order_products_file:
        orders = OrderProductTable.from_csv(order_products_file)

        for row in orders.dict_records():
            # skip the products of which the department cannot be found
            if row["product_id"] not in product_departments:
                continue

            # count order for the department
            department_id = product_departments[row["product_id"]]
            department_statics.add_order_count(department_id)

            # count first order for the department
            if not row["reordered"]:
                department_statics.add_first_order_count(department_id)

    return department_statics


def analyze_purchases(order_products_path, products_path, report_path):
    """
    Calculate, for each department, the number of times a product was requested,
    number of times a product was requested for the first time and a ratio of those two numbers.
    Save the result into a report csv file.

    :param order_products_path: str, path of the csv file holds order records
    :param products_path: str, path of the csv file holds product records
    :param report_path: str, path of the report csv file to be created
    :return: None
    """
    product_departments = extract_product_departments(products_path)
    department_statics = count_department_orders(order_products_path, product_departments)
    department_statics.to_data_table().to_csv(report_path)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Usage: python ./src/purchase_analytics.py "
              "./input/order_products.csv ./input/products.csv "
              "./output/report.csv")
        exit()

    order_products_path = sys.argv[1]
    products_path = sys.argv[2]
    report_path = sys.argv[3]

    if not os.access(order_products_path, os.R_OK):
        print("Cannot access file "+order_products_path)
        exit()
    if not os.access(products_path, os.R_OK):
        print("Cannot access file "+products_path)
        exit()

    analyze_purchases(order_products_path, products_path, report_path)
