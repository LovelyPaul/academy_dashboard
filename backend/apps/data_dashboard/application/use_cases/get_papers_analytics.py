"""
Get Papers Analytics Use Case

Orchestrates the retrieval of papers analytics data with filters.
"""

from typing import Dict, Optional
from core.exceptions import ValidationError
from apps.data_dashboard.domain.services.papers_service import PapersAnalyticsService
from apps.data_dashboard.infrastructure.repositories.papers_repository import PapersAnalyticsRepository


class GetPapersAnalyticsUseCase:
    """Use case for getting papers analytics data."""

    def __init__(self):
        """Initialize use case with repository and service."""
        self.repository = PapersAnalyticsRepository()
        self.service = PapersAnalyticsService(self.repository)

    def execute(
        self,
        year: Optional[int] = None,
        journal_grade: Optional[str] = None,
        field: Optional[str] = None
    ) -> Dict:
        """
        Execute the use case.

        Args:
            year: Filter by year
            journal_grade: Filter by journal grade
            field: Filter by department/field

        Returns:
            Analytics data dictionary containing:
            {
                "yearly_data": [...],
                "journal_data": [...],
                "field_data": [...],
                "has_data": bool
            }

        Raises:
            ValidationError: If filters are invalid
        """
        # Validate filters
        if not self.service.validate_filters(year, journal_grade, field):
            raise ValidationError(
                "Invalid filter parameters"
            )

        # Get analytics data
        analytics_data = self.service.get_analytics(
            year, journal_grade, field
        )

        # Check if data exists
        has_data = (
            len(analytics_data['yearly_data']) > 0 or
            len(analytics_data['journal_data']) > 0 or
            len(analytics_data['field_data']) > 0
        )

        return {
            **analytics_data,
            "has_data": has_data
        }
