"""
Papers Analytics Repository

Provides data access layer for publications table with filtering and aggregation.
"""

from typing import List, Dict, Optional
from django.db.models import Count, Q, QuerySet
from django.db.models.functions import ExtractYear
from apps.data_dashboard.models import Publication


class PapersAnalyticsRepository:
    """Repository for papers analytics data access."""

    def __init__(self):
        self.model = Publication

    def get_yearly_data(
        self,
        year: Optional[int] = None,
        journal_grade: Optional[str] = None,
        field: Optional[str] = None
    ) -> List[Dict]:
        """
        Get yearly publication counts.

        Args:
            year: Filter by specific year
            journal_grade: Filter by journal grade
            field: Filter by department/field

        Returns:
            List of dictionaries: [{"year": 2021, "count": 45}, ...]
        """
        queryset = self._apply_filters(
            self.model.objects.all(),
            year, journal_grade, field
        )

        result = (
            queryset
            .annotate(year=ExtractYear('publication_date'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )

        return list(result)

    def get_journal_distribution(
        self,
        year: Optional[int] = None,
        journal_grade: Optional[str] = None,
        field: Optional[str] = None
    ) -> List[Dict]:
        """
        Get journal grade distribution.

        Args:
            year: Filter by specific year
            journal_grade: Filter by journal grade
            field: Filter by department/field

        Returns:
            List of dictionaries: [{"journal_grade": "SCI", "count": 80}, ...]
        """
        queryset = self._apply_filters(
            self.model.objects.all(),
            year, journal_grade, field
        )

        result = (
            queryset
            .values('journal_grade')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return list(result)

    def get_field_statistics(
        self,
        year: Optional[int] = None,
        journal_grade: Optional[str] = None,
        field: Optional[str] = None
    ) -> List[Dict]:
        """
        Get field-wise publication statistics.

        Args:
            year: Filter by specific year
            journal_grade: Filter by journal grade
            field: Filter by department/field

        Returns:
            List of dictionaries: [{"department": "공학부", "count": 67}, ...]
        """
        queryset = self._apply_filters(
            self.model.objects.all(),
            year, journal_grade, field
        )

        result = (
            queryset
            .values('department')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return list(result)

    def _apply_filters(
        self,
        queryset: QuerySet,
        year: Optional[int],
        journal_grade: Optional[str],
        field: Optional[str]
    ) -> QuerySet:
        """
        Apply filters to queryset.

        Args:
            queryset: Base queryset
            year: Year filter
            journal_grade: Journal grade filter
            field: Field/department filter

        Returns:
            Filtered queryset
        """
        if year:
            queryset = queryset.filter(
                publication_date__year=year
            )

        if journal_grade:
            queryset = queryset.filter(
                journal_grade__iexact=journal_grade
            )

        if field:
            queryset = queryset.filter(
                department__icontains=field
            )

        return queryset
