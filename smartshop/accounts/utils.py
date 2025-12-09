"""
Utility functions for accounts app.
"""
import re


def normalize_phone_number(phone_number):
    """
    Normalize phone number to standard format without spaces and parentheses.

    Examples:
        +7 (777) 162-40-27 -> +77771624027
        +7 777 162 40 27 -> +77771624027
        +77771624027 -> +77771624027
    """
    if not phone_number:
        return phone_number

    # Remove all non-digit characters except the leading +
    normalized = re.sub(r'[^\d+]', '', phone_number)

    # Ensure it starts with +
    if not normalized.startswith('+'):
        normalized = '+' + normalized

    return normalized
