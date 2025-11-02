"""
StudentAnalyticsService: Business logic for student analytics calculations.
Pure business logic layer following SOLID principles.
No direct database access - uses data passed from repository.
"""
from typing import Dict, List
from decimal import Decimal
from core.exceptions import ValidationError


class StudentAnalyticsService:
    """Service for student analytics business logic."""

    @staticmethod
    def calculate_statistics(department_stats: List[Dict]) -> Dict:
        """
        Calculate aggregate statistics from department data.

        Args:
            department_stats: List of department statistics

        Returns:
            Dictionary with total, average, max department
        """
        if not department_stats:
            return {
                'total_students': 0,
                'department_count': 0,
                'average_per_department': 0,
                'largest_department': None
            }

        total_students = sum(dept['student_count'] for dept in department_stats)
        department_count = len(department_stats)
        average = total_students / department_count if department_count > 0 else 0

        largest = max(department_stats, key=lambda x: x['student_count'])

        return {
            'total_students': total_students,
            'department_count': department_count,
            'average_per_department': round(average, 1),
            'largest_department': largest['department']
        }

    @staticmethod
    def format_grade_distribution(grade_data: List[Dict]) -> List[Dict]:
        """
        Format grade distribution data with percentages.

        Args:
            grade_data: Raw grade distribution from repository

        Returns:
            Formatted data with percentage calculations
        """
        total = sum(item['count'] for item in grade_data)

        if total == 0:
            return []

        result = []
        for item in grade_data:
            percentage = (item['count'] / total) * 100
            result.append({
                'program_type': item['program_type'],
                'grade': item['grade'],
                'count': item['count'],
                'percentage': round(percentage, 1)
            })

        return result

    @staticmethod
    def validate_filters(filters: Dict) -> Dict:
        """
        Validate and sanitize filter parameters.

        Args:
            filters: Raw filter parameters from request

        Returns:
            Validated and sanitized filters

        Raises:
            ValidationError: If filters are invalid
        """
        validated = {}

        # Validate department
        if 'department' in filters and filters['department']:
            validated['department'] = str(filters['department'])

        # Validate grade (0-4)
        if 'grade' in filters and filters['grade'] is not None:
            try:
                grade = int(filters['grade'])
                if not (0 <= grade <= 4):
                    raise ValidationError("Grade must be between 0 and 4")
                validated['grade'] = grade
            except (ValueError, TypeError):
                raise ValidationError("Invalid grade format")

        # Validate year (2000-2100)
        if 'year' in filters and filters['year']:
            try:
                year = int(filters['year'])
                if not (2000 <= year <= 2100):
                    raise ValidationError("Year must be between 2000 and 2100")
                validated['year'] = year
            except (ValueError, TypeError):
                raise ValidationError("Invalid year format")

        return validated
