import csv
import os
import tempfile
import unittest

from payroll.calculator import calculate_payslip
from payroll.report import load_employees, write_report

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReportTests(unittest.TestCase):
    def test_import_reports_bad_rows(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "e.csv")
            with open(f, "w") as fh:
                fh.write("name,basic\nAnn,5000\nBob,-1\n,300\nCy,abc\n")
            emps, errors = load_employees(f)
        self.assertEqual([e.name for e in emps], ["Ann"])
        self.assertEqual(len(errors), 3)

    def test_report_roundtrip(self):
        emps, errors = load_employees(os.path.join(ROOT, "employees.csv"))
        self.assertEqual(errors, [])
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "r.csv")
            write_report(out, [calculate_payslip(e) for e in emps])
            with open(out, newline="") as fh:
                rows = list(csv.reader(fh))
        self.assertEqual(rows[0][0], "Name")
        self.assertEqual(rows[-1][0], "TOTAL")
        self.assertEqual(len(rows), len(emps) + 3)


if __name__ == "__main__":
    unittest.main()
