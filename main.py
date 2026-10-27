"""Simple GUI entry point for the payroll app."""
import sys

from payroll.gui import run


def main():
    run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
