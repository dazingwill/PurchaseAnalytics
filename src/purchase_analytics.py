
import csv
import time
import sys
import os
from src.dataframe import TableProcessor


def load_product_department(csv_file):
    products = TableProcessor().load_csv(csv_file)

    product_id_i = products.header_index["product_id"]
    department_id_i = products.header_index["department_id"]
    product_departments = {}
    for row in products:
        product_id = int(row[product_id_i])
        department_id = int(row[department_id_i])
        product_departments[product_id] = department_id
    return product_departments


def analyze_department_orders(departments, orders):
    department_statics = {}
    for department_id in departments:
        department_statics[department_id] = {
            "department_id": department_id,
            "number_of_orders": 0,
            "number_of_first_orders": 0
        }
    product_id_i = orders.header_index["product_id"]
    reordered_i = orders.header_index["reordered"]
    for row in orders:
        product_id = int(row[product_id_i])
        if product_id not in product_departments:
            continue
        department_id = product_departments[product_id]
        department_statics[department_id]["number_of_orders"] += 1
        is_first_order = row[reordered_i] == '0'
        if is_first_order:
            department_statics[department_id]["number_of_first_orders"] += 1
    return department_statics

def write_report(report_path, department_statics):
    output_headers = ["department_id", "number_of_orders", "number_of_first_orders", "percentage"]
    output_data = []
    for department_id in ordered_departments:
        order_num = department_statics[department_id]["number_of_orders"]
        if order_num == 0:
            continue

        first_order_num = department_statics[department_id]["number_of_first_orders"]
        ratio = "{:.2f}".format(first_order_num / order_num)

        output_data.append([department_id, order_num, first_order_num, ratio])
    outputer = TableProcessor(output_headers, output_data)
    outputer.to_csv(report_path)


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

    with open(products_path, "r", encoding="utf-8") as products_file:
        product_departments = load_product_department(products_file)
    departments = set(product_departments.values())
    ordered_departments = sorted(list(departments))

    end_time = time.time()
    print("program running time: " + str(end_time - start_time))

    with open(order_products_path, "r", encoding="utf-8") as order_products_file:
        orders = TableProcessor().load_csv(order_products_file)
        department_statics = analyze_department_orders(product_departments, orders)

    end_time = time.time()
    print("program running time: " + str(end_time - start_time))

    # output
    write_report(report_path, department_statics)

    end_time = time.time()
    print("program running time: "+str(end_time-start_time))






