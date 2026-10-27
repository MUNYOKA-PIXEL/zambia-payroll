"""Simple desktop interface for calculating payslips."""
import tkinter as tk
from tkinter import messagebox, ttk

from .rates import CURRENCY
from .calculator import Employee, calculate_payslip
from .validation import ValidationError

FIELDS = [("name", "Employee name"), ("basic", f"Basic salary ({CURRENCY})"),
          ("allowances", "Allowances"), ("overtime", "Overtime"),
          ("other_deductions", "Other deductions (loans etc.)")]
COLS = [("name", "Name", 170), ("gross", f"Gross ({CURRENCY})", 90), ("paye", "PAYE", 90),
        ("napsa_employee", "NAPSA", 80), ("nhima_employee", "NHIMA", 80),
        ("total_deductions", "Deductions", 100), ("net", "Net Pay", 100)]


class PayrollApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zambia Payroll Calculator")
        self.geometry("860x560")
        self.payslips = []
        self.vars = {k: tk.StringVar() for k, _ in FIELDS}
        self._build()

    def _build(self):
        form = ttk.LabelFrame(self, text="Employee", padding=10)
        form.pack(fill="x", padx=10, pady=8)

        for i, (key, label) in enumerate(FIELDS):
            ttk.Label(form, text=label).grid(row=i // 3, column=(i % 3) * 2, sticky="w", padx=4, pady=3)
            ttk.Entry(form, textvariable=self.vars[key], width=20).grid(
                row=i // 3, column=(i % 3) * 2 + 1, padx=4, pady=3)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=6, pady=(8, 0), sticky="w")
        for text, cmd in [("Calculate", self.preview), ("Add to payroll", self.add),
                          ("Remove selected", self.remove), ("Clear all", self.clear_all)]:
            ttk.Button(btns, text=text, command=cmd).pack(side="left", padx=3)

        self.detail = tk.Text(self, height=10, state="disabled", font=("Consolas", 10))
        self.detail.pack(fill="x", padx=10)

        self.tree = ttk.Treeview(self, columns=[c for c, _, _ in COLS], show="headings", height=8)
        for key, title, width in COLS:
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor="w" if key == "name" else "e")
        self.tree.pack(fill="both", expand=True, padx=10, pady=8)

    def _read_form(self):
        return Employee.from_input(*(self.vars[k].get() for k, _ in FIELDS))

    def _show(self, p):
        lines = [
            f"{p['name']}", "-" * 44,
            f"Gross pay             {p['gross']:>14,.2f} {CURRENCY}",
            f"Chargeable pay        {p['chargeable']:>14,.2f} {CURRENCY}",
            f"PAYE                  {p['paye']:>14,.2f} {CURRENCY}",
            f"NAPSA (5%)            {p['napsa_employee']:>14,.2f} {CURRENCY}",
            f"NHIMA (1% of basic)   {p['nhima_employee']:>14,.2f} {CURRENCY}",
            f"Other deductions      {p['other_deductions']:>14,.2f} {CURRENCY}",
            f"NET PAY               {p['net']:>14,.2f} {CURRENCY}",
            f"Employer cost (incl. NAPSA, NHIMA, SDL) {p['employer_cost']:,.2f} {CURRENCY}",
        ]
        self.detail.config(state="normal")
        self.detail.delete("1.0", "end")
        self.detail.insert("end", "\n".join(lines))
        self.detail.config(state="disabled")

    def preview(self):
        try:
            self._show(calculate_payslip(self._read_form()))
        except ValidationError as e:
            messagebox.showerror("Invalid input", str(e))

    def _add_row(self, p):
        self.payslips.append(p)
        self.tree.insert("", "end", values=[
            p[c] if c == "name" else f"{p[c]:,.2f} {CURRENCY}" for c, _, _ in COLS
        ])

    def add(self):
        try:
            p = calculate_payslip(self._read_form())
        except ValidationError as e:
            messagebox.showerror("Invalid input", str(e))
            return
        self._show(p)
        self._add_row(p)
        for v in self.vars.values():
            v.set("")

    def remove(self):
        for item in self.tree.selection():
            idx = self.tree.index(item)
            self.tree.delete(item)
            del self.payslips[idx]

    def clear_all(self):
        self.tree.delete(*self.tree.get_children())
        self.payslips.clear()


def run():
    PayrollApp().mainloop()
