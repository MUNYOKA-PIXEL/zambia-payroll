"""Input validation. Everything that enters the calculator passes through here."""
import re
from decimal import Decimal, InvalidOperation

from .rates import MAX_MONTHLY_AMOUNT


class ValidationError(ValueError):
    """Raised with a user-friendly message when input is invalid."""


def parse_money(value, field, required=False):
    """Convert user input ('K 5,200.50', '5200', 5200) to a Decimal >= 0."""
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            raise ValidationError(f"{field} is required.")
        return Decimal("0")
    if isinstance(value, bool):
        raise ValidationError(f"{field} must be a number.")
    text = str(value).strip()
    text = re.sub(r"(?i)^(zmw|zk|k)\s*", "", text)   # strip currency prefix
    text = text.replace(",", "").replace(" ", "")
    try:
        amount = Decimal(text)
    except InvalidOperation:
        raise ValidationError(f"{field} must be a number (got '{value}').")
    if not amount.is_finite():
        raise ValidationError(f"{field} must be a finite number.")
    if amount < 0:
        raise ValidationError(f"{field} cannot be negative.")
    if amount > MAX_MONTHLY_AMOUNT:
        raise ValidationError(f"{field} is unrealistically large.")
    if amount.as_tuple().exponent < -2:
        raise ValidationError(f"{field} can have at most 2 decimal places.")
    return amount


def parse_name(value):
    name = (value or "").strip()
    if not name:
        raise ValidationError("Employee name is required.")
    if len(name) > 100:
        raise ValidationError("Employee name is too long.")
    return name
