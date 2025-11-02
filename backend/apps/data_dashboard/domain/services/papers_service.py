"""
Papers Analytics Service

Business logic for papers analytics aggregation and data transformation.
"""

from typing import Dict, List, Optional
from apps.data_dashboard.infrastructure.repositories.papers_repository import PapersAnalyticsRepository


class PapersAnalyticsService:
    """Domain service for papers analytics business logic."""

    def __init__(self, repository: PapersAnalyticsRepository):
        """
        Initialize service with repository.

        Args:
            repository: PapersAnalyticsRepository instance
        """
        self.repository = repository

    def get_analytics(
        self,
        year: Optional[int] = None,
        journal_grade: Optional[str] = None,
        field: Optional[str] = None
    ) -> Dict:
        """
        Get complete papers analytics data.

        Args:
            year: Filter by specific year
            journal_grade: Filter by journal grade
            field: Filter by department/field

        Returns:
            Dictionary containing:
            {
                "yearly_data": [...],
                "journal_data": [...],
                "field_data": [...]
            }
        """
        yearly_data = self.repository.get_yearly_data(
            year, journal_grade, field
        )

        journal_data = self.repository.get_journal_distribution(
            year, journal_grade, field
        )

        field_data = self.repository.get_field_statistics(
            year, journal_grade, field
        )

        return {
            "yearly_data": yearly_data,
            "journal_data": journal_data,
            "field_data": field_data
        }

    def validate_filters(
        self,
        year: Optional[int],
        journal_grade: Optional[str],
        field: Optional[str]
    ) -> bool:
        """
        Validate filter parameters.

        Args:
            year: Year to validate
            journal_grade: Journal grade to validate
            field: Field to validate

        Returns:
            True if filters are valid, False otherwise
        """
        if year is not None and (year < 2000 or year > 2100):
            return False

        if journal_grade is not None and journal_grade not in ['SCI', 'KCI', 'SCOPUS', '기타']:
            return False

        return True
