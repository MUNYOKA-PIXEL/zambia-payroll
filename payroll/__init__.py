"""Zambia payroll calculator package.

This package implements payroll calculations and validation for a simplified
monthly Zambia payslip workflow.
"""

from .calculator import Employee, calculate_paye, calculate_payslip

__all__ = ["Employee", "calculate_paye", "calculate_payslip"]
__version__ = "0.1.0"
