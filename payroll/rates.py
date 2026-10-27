"""Statutory rates for Zambia. This is the ONLY file to edit when rates change.

Effective: 1 January 2026 (Income Tax (Amendment) Act No. 17 of 2025).
Sources used when this was written (October 2026): KPMG Zambia "2026 Budget
Highlights" (PAYE bands unchanged from 2025), plus 2026 NAPSA/NHIMA guides.
Published guides disagree on some figures, so ALWAYS confirm against ZRA
(zra.org.zm), NAPSA (napsa.co.zm) and NHIMA (nhima.co.zm) before running real
payroll, and update the values below.
"""
from decimal import Decimal as D

RATES_EFFECTIVE_FROM = "2026-01-01"
CURRENCY = "ZMW"

# Monthly PAYE bands: (upper limit of band, rate). None = no upper limit.
PAYE_BANDS_MONTHLY = [
    (D("5100"), D("0.00")),   # first K5,100 tax-free
    (D("7100"), D("0.20")),   # K5,100.01 - K7,100
    (D("9200"), D("0.30")),   # K7,100.01 - K9,200
    (None,      D("0.37")),   # above K9,200
]

# NAPSA: 5% employee + 5% employer on gross, up to an insurable ceiling.
NAPSA_EMPLOYEE_RATE = D("0.05")
NAPSA_EMPLOYER_RATE = D("0.05")
NAPSA_MONTHLY_CEILING = D("37236")   # = max K1,861.80 per side per month

# NHIMA: 1% employee + 1% employer on BASIC pay, no cap.
NHIMA_EMPLOYEE_RATE = D("0.01")
NHIMA_EMPLOYER_RATE = D("0.01")

# Skills Development Levy: employer only, 0.5% of gross.
SDL_EMPLOYER_RATE = D("0.005")

# Is the employee's NAPSA contribution deducted before PAYE is applied?
# Guides disagree. True = chargeable pay is gross minus NAPSA (Income Tax Act
# s.37 pension deduction). Set to False if your accountant says otherwise.
NAPSA_REDUCES_TAXABLE_PAY = True

# Sanity limit used by input validation (monthly amounts).
MAX_MONTHLY_AMOUNT = D("10000000")
