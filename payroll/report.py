"""CSV import/export."""
import csv

from .calculator import Employee, calculate_payslip
from .validation import ValidationError

REPORT_COLUMNS = [
    ("name", "Name"), ("basic", "Basic"), ("allowances", "Allowances"),
    ("overtime", "Overtime"), ("gross", "Gross"), ("paye", "PAYE"),
    ("napsa_employee", "NAPSA (Employee)"), ("nhima_employee", "NHIMA (Employee)"),
    ("other_deductions", "Other Deductions"), ("total_deductions", "Total Deductions"),
    ("net", "Net Pay"), ("napsa_employer", "NAPSA (Employer)"),
    ("nhima_employer", "NHIMA (Employer)"), ("sdl", "SDL (Employer)"),
    ("employer_cost", "Total Employer Cost"),
]


def load_employees(path):
    """Read employees from CSV. Columns: name,basic[,allowances,overtime,other_deductions].

    Returns (employees, errors). Bad rows are reported, not silently skipped.
    """
    employees, errors = [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {"name", "basic"} <= {c.strip().lower() for c in reader.fieldnames}:
            raise ValidationError("CSV must have at least 'name' and 'basic' columns.")
        for line_no, row in enumerate(reader, start=2):
            row = {(k or "").strip().lower(): v for k, v in row.items()}
            try:
                employees.append(Employee.from_input(
                    row.get("name"), row.get("basic"), row.get("allowances"),
                    row.get("overtime"), row.get("other_deductions")))
            except ValidationError as e:
                errors.append(f"Row {line_no}: {e}")
    return employees, errors


def write_report(path, payslips):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([label for _, label in REPORT_COLUMNS])
        for p in payslips:
            w.writerow([p[key] for key, _ in REPORT_COLUMNS])
        w.writerow([])
        w.writerow(["TOTAL"] + [
            sum(p[k] for p in payslips) if k != "name" else ""
            for k, _ in REPORT_COLUMNS[1:]])
