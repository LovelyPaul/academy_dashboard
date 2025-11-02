"""
Data formatting utility functions.
Following the common-modules.md specification.
"""
from datetime import datetime, date
from typing import Union


def format_currency(amount: int) -> str:
    """
    Format amount to Korean currency format.

    Args:
        amount: Amount in integer

    Returns:
        Formatted string (e.g., "1,000,000원")
    """
    return f"{amount:,}원"


def format_percentage(value: float) -> str:
    """
    Format value to percentage format.

    Args:
        value: Percentage value (e.g., 85.5)

    Returns:
        Formatted string (e.g., "85.5%")
    """
    return f"{value}%"


def format_date(date_obj: Union[date, datetime]) -> str:
    """
    Format date to Korean format.

    Args:
        date_obj: Date or datetime object

    Returns:
        Formatted string (e.g., "2024년 1월 1일")
    """
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    return date_obj.strftime("%Y년 %m월 %d일")


def format_number(number: Union[int, float]) -> str:
    """
    Format number with thousand separators.

    Args:
        number: Number to format

    Returns:
        Formatted string (e.g., "1,000,000")
    """
    return f"{number:,}"
