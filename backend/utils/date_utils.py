"""
Date utility functions.
Following the common-modules.md specification.
"""
from datetime import datetime, timedelta
from typing import List
import pandas as pd


def get_current_year() -> int:
    """
    Get current year.

    Returns:
        Current year as integer
    """
    return datetime.now().year


def get_date_range(start_date: str, end_date: str) -> List[datetime]:
    """
    Generate date range between start and end dates.

    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)

    Returns:
        List of datetime objects
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    return date_range.tolist()


def parse_date_string(date_string: str, format: str = "%Y-%m-%d") -> datetime:
    """
    Parse date string to datetime object.

    Args:
        date_string: Date string to parse
        format: Date format (default: "%Y-%m-%d")

    Returns:
        Datetime object
    """
    return datetime.strptime(date_string, format)


def get_year_start_end(year: int) -> tuple:
    """
    Get start and end dates for a given year.

    Args:
        year: Year

    Returns:
        Tuple of (start_date, end_date)
    """
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    return start_date, end_date


def get_quarter_dates(year: int, quarter: int) -> tuple:
    """
    Get start and end dates for a given quarter.

    Args:
        year: Year
        quarter: Quarter (1-4)

    Returns:
        Tuple of (start_date, end_date)
    """
    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Quarter must be between 1 and 4")

    quarter_start_month = {1: 1, 2: 4, 3: 7, 4: 10}
    start_month = quarter_start_month[quarter]
    start_date = datetime(year, start_month, 1)

    if quarter == 4:
        end_date = datetime(year, 12, 31)
    else:
        next_quarter_month = quarter_start_month[quarter + 1]
        end_date = datetime(year, next_quarter_month, 1) - timedelta(days=1)

    return start_date, end_date
