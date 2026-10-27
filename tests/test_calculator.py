import unittest
from decimal import Decimal as D
from unittest import mock

from payroll import rates
from payroll.calculator import Employee, calculate_paye, calculate_payslip
from payroll.validation import ValidationError, parse_money


def slip(basic, **kw):
    return calculate_payslip(Employee.from_input("Test", basic, **kw))


class PayeTests(unittest.TestCase):
    def test_progressive_bands(self):
        cases = [("0", "0.00"), ("5100", "0.00"),
                 ("7100", "400.00"),     # 2,000 x 20%
                 ("9200", "1030.00"),    # + 2,100 x 30%
                 ("10000", "1326.00")]   # + 800 x 37%
        for chargeable, expected in cases:
            with self.subTest(chargeable=chargeable):
                self.assertEqual(calculate_paye(D(chargeable)), D(expected))

    def test_no_cliff_at_band_edge(self):
        diff = calculate_paye(D("7100.01")) - calculate_paye(D("7100"))
        self.assertLess(diff, D("0.01"))


class PayslipTests(unittest.TestCase):
    def test_low_earner_pays_no_paye(self):
        p = slip("4000")
        self.assertEqual(p["paye"], 0)
        self.assertEqual(p["napsa_employee"], D("200.00"))
        self.assertEqual(p["nhima_employee"], D("40.00"))
        self.assertEqual(p["net"], D("3760.00"))

    def test_known_values(self):
        p = slip("10000")  # NAPSA 500 -> chargeable 9,500
        self.assertEqual(p["chargeable"], D("9500.00"))
        self.assertEqual(p["paye"], D("1141.00"))
        self.assertEqual(p["nhima_employee"], D("100.00"))
        self.assertEqual(p["net"], D("8259.00"))

    def test_napsa_capped(self):
        p = slip("80000")
        self.assertEqual(p["napsa_employee"], D("1861.80"))
        self.assertEqual(p["napsa_employer"], D("1861.80"))

    def test_nhima_on_basic_only(self):
        p = slip("10000", allowances="5000")
        self.assertEqual(p["nhima_employee"], D("100.00"))
        self.assertEqual(p["gross"], D("15000.00"))

    def test_employer_cost(self):
        self.assertEqual(slip("10000")["employer_cost"], D("10650"))

    def test_other_deductions(self):
        self.assertEqual(slip("10000", other_deductions="300")["net"], D("7959.00"))

    def test_napsa_flag_off(self):
        with mock.patch.object(rates, "NAPSA_REDUCES_TAXABLE_PAY", False):
            self.assertEqual(slip("10000")["paye"], D("1326.00"))

    def test_net_plus_deductions_equals_gross(self):
        for basic in ("1", "5100", "9200.50", "37236", "250000"):
            with self.subTest(basic=basic):
                p = slip(basic)
                self.assertEqual(p["net"] + p["total_deductions"], p["gross"])


class ValidationTests(unittest.TestCase):
    def test_bad_money_rejected(self):
        for bad in ["-5", "abc", "NaN", "Infinity", "1e999", "10.123", "99999999999"]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                parse_money(bad, "Amount")

    def test_formats_accepted(self):
        for good, expected in [("5,200.50", "5200.50"), ("K 4500", "4500"),
                               ("ZMW3000", "3000"), (" 100 ", "100")]:
            with self.subTest(good=good):
                self.assertEqual(parse_money(good, "Amount"), D(expected))

    def test_blank_optional_is_zero(self):
        self.assertEqual(parse_money("", "Allowances"), 0)

    def test_employee_rejects_bad_input(self):
        for kw in [dict(name="", basic="1000"), dict(name="A", basic=""),
                   dict(name="A", basic="0"),
                   dict(name="A", basic="1000", other_deductions="5000")]:
            with self.subTest(kw=kw), self.assertRaises(ValidationError):
                Employee.from_input(**kw)


if __name__ == "__main__":
    unittest.main()
