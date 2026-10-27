# Zambia Payroll Calculator

A simple Python desktop application that calculates monthly payroll figures for employees using configurable Zambia payroll assumptions.

## What the app does

- Accepts an employee name, basic salary, allowances, overtime, and other deductions.
- Calculates gross pay, chargeable pay, PAYE, employee NAPSA and NHIMA deductions, net pay, and employer costs.
- Lets you preview a payslip, add it to the payroll list, remove selected employees, or clear the list.
- Checks inputs and displays an error if required information or amounts are invalid.

## Payroll assumptions

The current rates and calculation settings are in `payroll/rates.py`.

| Item | Current calculation |
|---|---|
| PAYE | Progressive monthly tax bands |
| NAPSA | 5% employee and 5% employer contribution, each subject to a monthly ceiling |
| NHIMA | 1% employee and 1% employer contribution on basic salary |
| Skills Development Levy (SDL) | 0.5% of gross pay, employer contribution |

The application is intended for a class project and demonstration. Payroll rules and rates can change; confirm current requirements with the relevant Zambian authorities before relying on any result for actual payroll.

## Project files

- `main.py` — starts the desktop application.
- `payroll/gui.py` — Tkinter user interface.
- `payroll/calculator.py` — employee model and payslip calculations.
- `payroll/validation.py` — input parsing and validation.
- `payroll/rates.py` — payroll rates and calculation settings.
- `payroll/report.py` — CSV import and report-writing helpers. These helpers are not currently available from the GUI.
- `tests/` — automated tests for calculations, validation, and CSV helpers.

## Requirements

- Python 3.9 or later
- Tkinter, which is included with most standard Python installations

## Run the application

Open a terminal in the `zambia-payroll` folder and run:

```powershell
python main.py
```

If the terminal is at the repository root, enter the project folder first:

```powershell
Set-Location .\zambia-payroll
python main.py
```

## Run the tests

Run the tests from the `zambia-payroll` folder:

```powershell
python -m unittest discover -v
```

## Notes

- The payroll list exists only while the application is open; it is not saved automatically.
- CSV import and export are not currently exposed in the desktop interface.
- This project does not provide employee accounts, payroll history, or persistent storage.
