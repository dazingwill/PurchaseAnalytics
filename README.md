# Purchase Analytics

## Background

See <https://github.com/InsightDataScience/Purchase-Analytics>

## Environment

Python 3 (I use Python 3.6)

## Usage

* generally, type:
  ```
  python3 path/to/purchase_analytics.py path/to/order_products.csv path/to/products.csv path/to/report.csv
  ```

* To run the script on files in `input` folder:

  run  `run.sh`

* To test the input/output test cases:

  run  `run_tests.sh` under folder `insight_testsuite` .

* To run all the tests:


  ```
  python3 insight_testsuite/my_test.py
  ```

## Performance

### Memory

The input records are read and processed line-by-line. The majority of the memory occupied should be the product-to-department dictionary with the one item for each products record.

### Time

For prior dataset, run time in my computer is around 50 seconds.

The most of the time consumed in operations on order records.

## Note

* I used csv library since it's a standard I/O library in Python.

* I assume there won't be duplicated products in one order.

* I assume there won't be any blank lines, tabs or typos in the input files.

* I don't assume the department IDs are continuous small numbers.

