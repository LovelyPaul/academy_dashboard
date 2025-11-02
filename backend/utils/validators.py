"""
Data validation utility functions.
Following the common-modules.md specification.
"""
import re
from typing import List


def validate_year(year: int) -> bool:
    """
    Validate year is within acceptable range.

    Args:
        year: Year to validate

    Returns:
        True if valid, False otherwise
    """
    return 2000 <= year <= 2100


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email string to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file extension is in allowed list.

    Args:
        filename: Name of file to validate
        allowed_extensions: List of allowed extensions (e.g., ['xlsx', 'xls'])

    Returns:
        True if valid, False otherwise
    """
    if not filename or '.' not in filename:
        return False

    extension = filename.rsplit('.', 1)[-1].lower()
    return extension in [ext.lower() for ext in allowed_extensions]


def validate_file_size(file_size: int, max_size_mb: int) -> bool:
    """
    Validate file size is within limit.

    Args:
        file_size: File size in bytes
        max_size_mb: Maximum allowed size in MB

    Returns:
        True if valid, False otherwise
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes
