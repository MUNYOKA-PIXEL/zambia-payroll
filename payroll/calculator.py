"""Pure calculation logic. No input/output here, so it is easy to test."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from . import rates as R
from .validation import ValidationError, parse_money, parse_name

CENT = Decimal("0.01")


def money(x):
    return Decimal(x).quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Employee:
    name: str
    basic: Decimal
    allowances: Decimal = Decimal("0")
    overtime: Decimal = Decimal("0")
    other_deductions: Decimal = Decimal("0")   # loans, advances, union dues

    @classmethod
    def from_input(cls, name, basic, allowances="", overtime="", other_deductions=""):
        """Build a validated Employee from raw (string) input."""
        emp = cls(
            name=parse_name(name),
            basic=parse_money(basic, "Basic salary", required=True),
            allowances=parse_money(allowances, "Allowances"),
            overtime=parse_money(overtime, "Overtime"),
            other_deductions=parse_money(other_deductions, "Other deductions"),
        )
        if emp.basic <= 0:
            raise ValidationError("Basic salary must be greater than zero.")
        if emp.other_deductions > emp.basic + emp.allowances + emp.overtime:
            raise ValidationError("Other deductions cannot exceed gross pay.")
        return emp


def calculate_paye(chargeable):
    """Progressive PAYE on monthly chargeable pay (each slice at its own rate)."""
    tax, lower = Decimal("0"), Decimal("0")
    for upper, rate in R.PAYE_BANDS_MONTHLY:
        top = chargeable if upper is None else min(chargeable, upper)
        if top > lower:
            tax += (top - lower) * rate
        if upper is None or chargeable <= upper:
            break
        lower = upper
    return money(tax)


def calculate_napsa(gross, rate):
    return money(min(gross, R.NAPSA_MONTHLY_CEILING) * rate)


def calculate_payslip(emp):
    """Return a dict with every figure for one employee for one month."""
    gross = emp.basic + emp.allowances + emp.overtime

    napsa_ee = calculate_napsa(gross, R.NAPSA_EMPLOYEE_RATE)
    nhima_ee = money(emp.basic * R.NHIMA_EMPLOYEE_RATE)

    chargeable = gross - napsa_ee if R.NAPSA_REDUCES_TAXABLE_PAY else gross
    paye = calculate_paye(chargeable)

    total_ded = paye + napsa_ee + nhima_ee + emp.other_deductions
    net = gross - total_ded

    napsa_er = calculate_napsa(gross, R.NAPSA_EMPLOYER_RATE)
    nhima_er = money(emp.basic * R.NHIMA_EMPLOYER_RATE)
    sdl = money(gross * R.SDL_EMPLOYER_RATE)

    return {
        "name": emp.name,
        "basic": money(emp.basic),
        "allowances": money(emp.allowances),
        "overtime": money(emp.overtime),
        "gross": money(gross),
        "chargeable": money(chargeable),
        "paye": paye,
        "napsa_employee": napsa_ee,
        "nhima_employee": nhima_ee,
        "other_deductions": money(emp.other_deductions),
        "total_deductions": money(total_ded),
        "net": money(net),
        "napsa_employer": napsa_er,
        "nhima_employer": nhima_er,
        "sdl": sdl,
        "employer_cost": money(gross + napsa_er + nhima_er + sdl),
    }
