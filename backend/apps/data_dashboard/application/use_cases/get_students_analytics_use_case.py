"""
GetStudentsAnalyticsUseCase: Orchestrates student analytics data retrieval.
Application layer that coordinates between domain services and repositories.
Follows the use case pattern from architecture.md.
"""
from typing import Dict
from apps.data_dashboard.infrastructure.repositories.student_repository import StudentRepository
from apps.data_dashboard.domain.services.student_analytics_service import StudentAnalyticsService
from core.exceptions import ValidationError, NotFoundError


class GetStudentsAnalyticsUseCase:
    """Use case for retrieving student analytics data."""

    def __init__(self):
        self.repository = StudentRepository()
        self.service = StudentAnalyticsService()

    def execute(self, filters: Dict) -> Dict:
        """
        Execute the use case to get student analytics.

        Args:
            filters: Dictionary of filter parameters

        Returns:
            Dictionary containing all analytics data

        Raises:
            ValidationError: If filters are invalid
            NotFoundError: If no data exists
        """
        # Step 1: Validate filters
        validated_filters = self.service.validate_filters(filters)

        # Step 2: Fetch data from repository
        department_stats = list(
            self.repository.get_department_stats(validated_filters)
        )
        grade_distribution = list(
            self.repository.get_grade_distribution(validated_filters)
        )
        enrollment_trend = self.repository.get_enrollment_trend(
            validated_filters
        )

        # Step 3: Format grade distribution with percentages
        formatted_grades = self.service.format_grade_distribution(
            grade_distribution
        )

        # Step 4: Return aggregated response
        return {
            'department_stats': department_stats,
            'grade_distribution': formatted_grades,
            'enrollment_trend': enrollment_trend
        }
