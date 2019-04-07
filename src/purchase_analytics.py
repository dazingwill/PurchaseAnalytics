import time
import sys
import os

from data_table import DepartmentStaticsTable, OrderProductTable, ProductTable


def extract_product_departments(products_path):
    with open(products_path, "r", encoding="utf-8") as products_file:
        product_records = ProductTable().load_csv(products_file)
        product_departments = {row["product_id"]: row["department_id"] for row in product_records.dict_records()}
        return product_departments


def count_department_orders(order_products_path, product_departments):
    departments = set(product_departments.values())
    department_statics = DepartmentStaticsTable(departments=departments)

    with open(order_products_path, "r", encoding="utf-8") as order_products_file:
        orders = OrderProductTable().load_csv(order_products_file)
        for row in orders.dict_records():
            if row["product_id"] not in product_departments:
                continue
            department_id = product_departments[row["product_id"]]
            department_statics.add_order_count(department_id)

            if not row["reordered"]:
                department_statics.add_first_order_count(department_id)

    return department_statics


def write_report(report_path, department_statics):
    department_statics.summarize()
    department_statics.to_csv(report_path)


def analyze_purchases(order_products_path, products_path, report_path):
    product_departments = extract_product_departments(products_path)
    department_statics = count_department_orders(order_products_path, product_departments)
    write_report(report_path, department_statics)


order_products_path = "./input/order_products.csv"
order_products_path = "./input/order_products__train.csv"
order_products_path = "./input/order_products__prior.csv"
products_path = "./input/products.csv"
report_path = "./output/report.csv"

if __name__ == '__main__':

    start_time = time.time()

    if len(sys.argv) < 4:
        print("Usage: python ./src/purchase_analytics.py "
              "./input/order_products.csv ./input/products.csv "
              "./output/report.csv")
        exit()

    # order_products_path = sys.argv[1]
    # products_path = sys.argv[2]
    # report_path = sys.argv[3]

    analyze_purchases(order_products_path, products_path, report_path)

    end_time = time.time()
    print("program running time: "+str(end_time-start_time))






