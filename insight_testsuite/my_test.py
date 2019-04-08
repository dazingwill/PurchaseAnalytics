import unittest
import os

from purchase_analytics import analyze_purchases
from data_table import DataTable, OrderProductTable, ProductTable, DepartmentStaticsTable


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


class MyTest(unittest.TestCase):

    FULL_TEST = False

    @classmethod
    def setUpClass(cls):
        cls.curr_path = os.path.dirname(os.path.realpath(__file__))
        cls.tests_path = os.path.join(cls.curr_path, "tests")
        cls.test_customized_path = os.path.join(cls.curr_path, "test_customized")
        cls.temp_report_path = os.path.join(cls.curr_path, "temp/output/report.csv")

    def setUp(self):
        pass

    def test_1(self):
        """test in sample dataset provided by Insight testsuite"""
        test_path = os.path.join(self.tests_path, "test_1")
        order_products_path = os.path.join(test_path, "input/order_products.csv")
        products_path = os.path.join(test_path, "input/products.csv")
        correct_report_path = os.path.join(test_path, "output/report.csv")

        analyze_purchases(order_products_path, products_path, self.temp_report_path)

        self.assertMultiLineEqual(read_file(self.temp_report_path), read_file(correct_report_path),
                                  "report file is not equal to the answer")

    def test_input_no_record(self):
        """test input files have no record"""
        test_path = os.path.join(self.tests_path, "test_input_no_record")
        order_products_path = os.path.join(test_path, "input/order_products.csv")
        products_path = os.path.join(test_path, "input/products.csv")
        correct_report_path = os.path.join(test_path, "output/report.csv")

        analyze_purchases(order_products_path, products_path, self.temp_report_path)

        self.assertMultiLineEqual(read_file(self.temp_report_path), read_file(correct_report_path),
                                  "report file is not equal to the answer")

    def test_input_extra_header(self):
        """test input files have a new column"""
        test_path = os.path.join(self.tests_path, "test_input_extra_header")
        order_products_path = os.path.join(test_path, "input/order_products.csv")
        products_path = os.path.join(test_path, "input/products.csv")
        correct_report_path = os.path.join(test_path, "output/report.csv")

        analyze_purchases(order_products_path, products_path, self.temp_report_path)

        self.assertMultiLineEqual(read_file(self.temp_report_path), read_file(correct_report_path),
                                  "report file is not equal to the answer")

    def test_train_dataset(self):
        """test in train dataset provided by Instacart"""
        test_path = os.path.join(self.tests_path, "test_train_dataset")
        order_products_path = os.path.join(test_path, "input/order_products.csv")
        products_path = os.path.join(test_path, "input/products.csv")
        correct_report_path = os.path.join(test_path, "output/report.csv")

        analyze_purchases(order_products_path, products_path, self.temp_report_path)

        self.assertMultiLineEqual(read_file(self.temp_report_path), read_file(correct_report_path),
                                  "report file is not equal to the answer")

    @unittest.skipUnless(FULL_TEST, "skip prior dataset to save time")
    def test_prior_dataset(self):
        """test in prior dataset provided by Instacart"""
        test_path = os.path.join(self.tests_path, "test_prior_dataset")
        order_products_path = os.path.join(test_path, "input/order_products.csv")
        products_path = os.path.join(test_path, "input/products.csv")
        correct_report_path = os.path.join(test_path, "output/report.csv")

        analyze_purchases(order_products_path, products_path, self.temp_report_path)

        self.assertMultiLineEqual(read_file(self.temp_report_path), read_file(correct_report_path),
                                  "report file is not equal to the answer")

    def test_miss_header(self):
        """test in input files miss a header"""
        order_products_path = os.path.join(self.test_customized_path, "order_products_miss_header.csv")
        products_path = os.path.join(self.test_customized_path, "products_miss_header.csv")
        with self.assertRaises(ValueError):
            OrderProductTable.from_csv(order_products_path)
        with self.assertRaises(ValueError):
            ProductTable.from_csv(products_path)

    def test_data_table(self):
        """test regular operations for DataTable"""
        with self.assertRaises(TypeError):
            DataTable("")
        with self.assertRaises(TypeError):
            DataTable(1, ["header1"])

        table = DataTable([[1, 2], [3]], ["header1", "header2"])
        rows = list(table.dict_records())
        self.assertEqual(rows[0]["header2"], 2)
        self.assertEqual(rows[1]["header1"], 3)
        with self.assertRaises(KeyError):
            a = rows[1]["header2"]

        table = DataTable([1, 2], ["header1", "header2"])
        with self.assertRaises(TypeError):
            rows = list(table)

    def test_department_statics_table(self):
        """test regular operations for DepartmentStaticsTable"""
        with self.assertRaises(TypeError):
            DepartmentStaticsTable()
        with self.assertRaises(TypeError):
            DepartmentStaticsTable(departments=5)

        correct_report_path = os.path.join(self.test_customized_path, "report_department_statics_table.csv")
        table = DepartmentStaticsTable([[0, 0, 0, 0], [1, 0, 0, 0]])
        table.add_order_count(1, 2)
        table.add_first_order_count(1)
        table.to_csv(self.temp_report_path)
        self.assertMultiLineEqual(read_file(self.temp_report_path), read_file(correct_report_path),
                                  "report file is not equal to the answer")


if __name__ == '__main__':
    unittest.main(verbosity=1)
