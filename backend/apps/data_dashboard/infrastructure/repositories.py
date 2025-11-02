"""
Dashboard Repository Module
Data access layer for dashboard queries following the plan.md specifications.
Implements all query methods for KPI, trend, department, and budget data.
"""
from django.db import models
from django.db.models import Avg, Sum, Count, Q, Max
from django.db.models.functions import ExtractYear
from datetime import datetime

from ..models import DepartmentKPI, Publication, Student, ResearchBudgetData
from backend.utils.date_utils import get_current_year


class DashboardRepository:
    """
    Repository for dashboard data queries.
    Provides data access methods for all dashboard metrics.
    """

    def get_latest_kpi_data(self):
        """
        Query latest year KPI data from department_kpis table.

        Returns:
            QuerySet of DepartmentKPI for the latest year
        """
        # Get the latest year that has data
        latest_year_obj = DepartmentKPI.objects.aggregate(
            max_year=Max('year')
        )
        latest_year = latest_year_obj['max_year']

        if latest_year is None:
            return DepartmentKPI.objects.none()

        return DepartmentKPI.objects.filter(year=latest_year)

    def get_publication_count_current_year(self):
        """
        Query publication count for current year.

        Returns:
            int: Total publication count for current year
        """
        current_year = get_current_year()

        count = Publication.objects.filter(
            publication_date__year=current_year
        ).count()

        return count

    def get_active_student_count(self):
        """
        Query count of students with enrollment_status = '재학'.

        Returns:
            int: Active student count
        """
        count = Student.objects.filter(
            enrollment_status='재학'
        ).count()

        return count

    def get_budget_summary(self):
        """
        Query budget totals and execution amounts.

        Returns:
            dict: {
                'total_budget': sum of total_budget,
                'executed_amount': sum of execution_amount where status='집행완료'
            }
        """
        # Get sum of distinct total_budget per project
        # Use DISTINCT on project_number to avoid double counting
        from django.db.models import Subquery, OuterRef

        # Subquery to get unique projects with their total_budget
        unique_projects = ResearchBudgetData.objects.filter(
            project_number=OuterRef('project_number')
        ).values('project_number').annotate(
            budget=Max('total_budget')
        ).values('budget')[:1]

        # Get total budget (sum of distinct project budgets)
        total_budget_result = ResearchBudgetData.objects.values('project_number').annotate(
            project_budget=Max('total_budget')
        ).aggregate(
            total=Sum('project_budget')
        )

        # Get executed amount (sum of all executions with status='집행완료')
        executed_result = ResearchBudgetData.objects.filter(
            status='집행완료'
        ).aggregate(
            total=Sum('execution_amount')
        )

        return {
            'total_budget': total_budget_result['total'] or 0,
            'executed_amount': executed_result['total'] or 0
        }

    def get_yearly_trends(self, start_year=None, end_year=None):
        """
        Query yearly KPI trends.

        Args:
            start_year (int): Starting year (default: 4 years ago)
            end_year (int): Ending year (default: current year)

        Returns:
            QuerySet: Yearly aggregated data with year, avg_employment_rate, total_revenue
        """
        current_year = get_current_year()

        if start_year is None:
            start_year = current_year - 3  # Last 4 years including current

        if end_year is None:
            end_year = current_year

        trends = DepartmentKPI.objects.filter(
            year__gte=start_year,
            year__lte=end_year
        ).values('year').annotate(
            avg_employment_rate=Avg('employment_rate'),
            total_revenue=Sum('tech_transfer_revenue')
        ).order_by('year')

        return trends

    def get_department_performance(self, year=None):
        """
        Query department performance for a given year.

        Args:
            year (int): Target year (default: latest year)

        Returns:
            QuerySet: Department aggregated performance
        """
        if year is None:
            # Get latest year
            latest_year_obj = DepartmentKPI.objects.aggregate(
                max_year=Max('year')
            )
            year = latest_year_obj['max_year']

            if year is None:
                return DepartmentKPI.objects.none()

        performance = DepartmentKPI.objects.filter(
            year=year
        ).values('department').annotate(
            avg_employment_rate=Avg('employment_rate'),
            total_revenue=Sum('tech_transfer_revenue')
        ).order_by('-avg_employment_rate')

        return performance

    def get_budget_allocation(self):
        """
        Query budget allocation by department.

        Returns:
            QuerySet: Department budget allocation with total_budget and executed_amount
        """
        # Group by department
        # For each department, get sum of distinct project budgets and sum of executions
        allocation = ResearchBudgetData.objects.values('department').annotate(
            total_budget=Sum('total_budget', distinct=True),
            executed_amount=Sum('execution_amount')
        ).order_by('-total_budget')

        return allocation


class PerformanceRepository:
    """
    Repository for performance analysis data access.
    Provides methods for retrieving performance metrics with filtering.
    """

    def get_performance_trend(self, start_date, end_date, department=None, project=None):
        """
        Get performance trend data over time period.

        Args:
            start_date (date): Start date for filtering
            end_date (date): End date for filtering
            department (str, optional): Department filter
            project (str, optional): Project filter (project_number)

        Returns:
            list: Performance trend data points
        """
        from django.db.models.functions import TruncMonth

        # Start with DepartmentKPI for performance metrics
        queryset = DepartmentKPI.objects.filter(
            year__gte=start_date.year,
            year__lte=end_date.year
        )

        # Apply department filter if provided
        if department:
            queryset = queryset.filter(department=department)

        # Group by month and aggregate
        trend_data = queryset.values('year').annotate(
            avg_employment_rate=Avg('employment_rate'),
            total_revenue=Sum('tech_transfer_revenue'),
            total_conferences=Sum('intl_conference_count')
        ).order_by('year')

        # Transform to expected format
        result = []
        for item in trend_data:
            # Use employment rate as the primary performance value
            value = float(item['avg_employment_rate']) if item['avg_employment_rate'] else 0.0

            result.append({
                'date': f"{item['year']}-01-01",  # Year start date
                'value': round(value, 2),
                'target': 85.0  # Default target of 85% employment rate
            })

        return result

    def get_department_comparison(self, start_date, end_date, project=None):
        """
        Get department-wise performance comparison.

        Args:
            start_date (date): Start date for filtering
            end_date (date): End date for filtering
            project (str, optional): Project filter

        Returns:
            list: Department comparison data
        """
        # Get department performance for the period
        queryset = DepartmentKPI.objects.filter(
            year__gte=start_date.year,
            year__lte=end_date.year
        )

        # Group by department and aggregate
        dept_data = queryset.values('department').annotate(
            avg_employment_rate=Avg('employment_rate'),
            total_revenue=Sum('tech_transfer_revenue')
        ).order_by('-avg_employment_rate')

        # Calculate total for percentage
        total_value = sum(
            float(item['avg_employment_rate']) if item['avg_employment_rate'] else 0.0
            for item in dept_data
        )

        # Transform to expected format
        result = []
        for item in dept_data:
            value = float(item['avg_employment_rate']) if item['avg_employment_rate'] else 0.0
            percentage = (value / total_value * 100) if total_value > 0 else 0.0

            result.append({
                'department': item['department'],
                'value': round(value, 2),
                'percentage': round(percentage, 2)
            })

        return result[:10]  # Return top 10 departments

    def get_achievement_rate(self, start_date, end_date, department=None):
        """
        Calculate achievement rate against targets.

        Args:
            start_date (date): Start date for filtering
            end_date (date): End date for filtering
            department (str, optional): Department filter

        Returns:
            dict: Achievement data with actual and target values
        """
        # Get performance data for the period
        queryset = DepartmentKPI.objects.filter(
            year__gte=start_date.year,
            year__lte=end_date.year
        )

        if department:
            queryset = queryset.filter(department=department)

        # Calculate aggregate metrics
        aggregates = queryset.aggregate(
            avg_employment=Avg('employment_rate'),
            total_revenue=Sum('tech_transfer_revenue')
        )

        # Use employment rate as primary metric
        actual_value = float(aggregates['avg_employment']) if aggregates['avg_employment'] else 0.0
        target_value = 85.0  # Target employment rate of 85%

        return {
            'actual': round(actual_value, 2),
            'target': target_value
        }


class PapersAnalyticsRepository:
    """
    Repository for papers analytics data access.
    Provides methods for retrieving publication statistics with filtering.
    """

    def __init__(self):
        self.model = Publication

    def get_yearly_data(self, year=None, journal_grade=None, field=None):
        """
        Get yearly publication counts.

        Args:
            year (int, optional): Filter by specific year
            journal_grade (str, optional): Filter by journal grade
            field (str, optional): Filter by department/field

        Returns:
            list: [{"year": 2021, "count": 45}, ...]
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

    def get_journal_distribution(self, year=None, journal_grade=None, field=None):
        """
        Get journal grade distribution.

        Args:
            year (int, optional): Filter by specific year
            journal_grade (str, optional): Filter by journal grade
            field (str, optional): Filter by department/field

        Returns:
            list: [{"journal_grade": "SCI", "count": 80}, ...]
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

    def get_field_statistics(self, year=None, journal_grade=None, field=None):
        """
        Get field-wise publication statistics.

        Args:
            year (int, optional): Filter by specific year
            journal_grade (str, optional): Filter by journal grade
            field (str, optional): Filter by department/field

        Returns:
            list: [{"department": "공학부", "count": 67}, ...]
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

    def _apply_filters(self, queryset, year, journal_grade, field):
        """
        Apply filters to queryset.

        Args:
            queryset: Base queryset
            year (int, optional): Year filter
            journal_grade (str, optional): Journal grade filter
            field (str, optional): Field/department filter

        Returns:
            QuerySet: Filtered queryset
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


class BudgetRepository:
    """
    Repository for budget data access.

    Provides abstracted database queries for budget analysis.
    All queries use Django ORM for database independence.
    """

    def get_budget_by_department(self, department=None, year=None, category=None):
        """
        Get aggregated budget data by department.

        Args:
            department (str, optional): Filter by specific department
            year (int, optional): Filter by year
            category (str, optional): Filter by category (execution_item)

        Returns:
            list: List of dicts with department, total_budget, project_count
        """
        queryset = ResearchBudgetData.objects.filter(
            status='집행완료'
        )

        # Apply filters
        if department:
            queryset = queryset.filter(department=department)

        if year:
            queryset = queryset.filter(
                execution_date__year=year
            )

        if category:
            queryset = queryset.filter(
                execution_item__icontains=category
            )

        # Aggregate by department
        result = queryset.values('department').annotate(
            total_budget=Sum('total_budget', distinct=True),
            project_count=Count('project_number', distinct=True)
        ).order_by('-total_budget')

        return list(result)

    def get_execution_by_department(self, department=None, year=None, start_date=None, end_date=None):
        """
        Get budget execution data by department.

        Args:
            department (str, optional): Filter by department
            year (int, optional): Filter by year
            start_date (date, optional): Start date for execution filter
            end_date (date, optional): End date for execution filter

        Returns:
            list: List of dicts with department, total_budget, executed_amount
        """
        queryset = ResearchBudgetData.objects.all()

        # Apply filters
        if department:
            queryset = queryset.filter(department=department)

        if year:
            queryset = queryset.filter(execution_date__year=year)

        if start_date:
            queryset = queryset.filter(execution_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(execution_date__lte=end_date)

        # Aggregate execution data
        from django.db.models import Case, When, Value

        result = queryset.values('department').annotate(
            total_budget=Sum('total_budget', distinct=True),
            executed_amount=Sum(
                Case(
                    When(status='집행완료', then='execution_amount'),
                    default=Value(0)
                )
            )
        ).order_by('department')

        return list(result)

    def get_yearly_trends(self, department=None, start_year=None, end_year=None):
        """
        Get year-over-year budget trends.

        Args:
            department (str, optional): Filter by department
            start_year (int, optional): Start year for trends
            end_year (int, optional): End year for trends

        Returns:
            list: List of dicts with year, total_budget, executed_amount
        """
        queryset = ResearchBudgetData.objects.all()

        if department:
            queryset = queryset.filter(department=department)

        # Extract year and aggregate
        queryset = queryset.annotate(
            year=ExtractYear('execution_date')
        )

        if start_year:
            queryset = queryset.filter(year__gte=start_year)

        if end_year:
            queryset = queryset.filter(year__lte=end_year)

        from django.db.models import Case, When, Value

        result = queryset.values('year').annotate(
            total_budget=Sum('total_budget', distinct=True),
            executed_amount=Sum(
                Case(
                    When(status='집행완료', then='execution_amount'),
                    default=Value(0)
                )
            )
        ).order_by('year')

        return list(result)


class DataUploadRepository:
    """
    Repository for data upload operations.
    Handles bulk upsert operations for all data models.
    Follows DIP: Domain layer depends on repository interface.
    """

    def bulk_upsert(self, model_class, data: list, unique_fields: list) -> int:
        """
        Bulk insert or update data using UPSERT strategy.

        Args:
            model_class: Django model class
            data: List of dictionaries with data
            unique_fields: List of fields that define uniqueness

        Returns:
            Number of records processed

        Raises:
            Exception: If database operation fails
        """
        from django.db import transaction

        if not data:
            return 0

        records_processed = 0

        with transaction.atomic():
            for item in data:
                # Create update_fields (all fields except unique ones)
                update_fields = {k: v for k, v in item.items() if k not in unique_fields}

                # Create lookup dict for unique fields
                lookup = {k: item[k] for k in unique_fields if k in item}

                # Use update_or_create
                obj, created = model_class.objects.update_or_create(
                    **lookup,
                    defaults=update_fields
                )
                records_processed += 1

        return records_processed

    def count_records(self, model_class, filters: dict = None) -> int:
        """
        Count records matching filters.

        Args:
            model_class: Django model class
            filters: Dictionary of filter conditions

        Returns:
            Count of matching records
        """
        queryset = model_class.objects.all()

        if filters:
            queryset = queryset.filter(**filters)

        return queryset.count()


class UploadHistoryRepository:
    """
    Repository for UploadHistory model.
    Manages upload history records.
    """

    def create_history(
        self,
        user_id: int,
        file_name: str,
        file_type: str,
        status: str,
        records_processed: int = 0,
        error_message: str = None
    ):
        """
        Create upload history record.

        Args:
            user_id: ID of user who uploaded
            file_name: Name of uploaded file
            file_type: Type of data file
            status: Upload status ('success' or 'failed')
            records_processed: Number of records processed
            error_message: Error message if failed

        Returns:
            Created UploadHistory instance
        """
        from ..models import UploadHistory
        from apps.users.models import User

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError(f"User with id {user_id} not found")

        history = UploadHistory.objects.create(
            user=user,
            file_name=file_name,
            file_type=file_type,
            status=status,
            records_processed=records_processed,
            error_message=error_message
        )

        return history

    def get_history_list(self, page: int = 1, page_size: int = 20):
        """
        Get paginated upload history.

        Args:
            page: Page number (1-indexed)
            page_size: Number of records per page

        Returns:
            QuerySet of UploadHistory
        """
        from ..models import UploadHistory

        offset = (page - 1) * page_size
        queryset = UploadHistory.objects.select_related('user').order_by('-uploaded_at')

        return queryset[offset:offset + page_size]

    def get_history_count(self):
        """
        Get total count of upload history records.

        Returns:
            Total count
        """
        from ..models import UploadHistory

        return UploadHistory.objects.count()

    def get_history_by_user(self, user_id: int, page: int = 1, page_size: int = 20):
        """
        Get history filtered by user.

        Args:
            user_id: User ID to filter by
            page: Page number (1-indexed)
            page_size: Number of records per page

        Returns:
            QuerySet of UploadHistory for specified user
        """
        from ..models import UploadHistory

        offset = (page - 1) * page_size
        queryset = UploadHistory.objects.filter(
            user_id=user_id
        ).select_related('user').order_by('-uploaded_at')

        return queryset[offset:offset + page_size]
