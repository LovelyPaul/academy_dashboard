"""
Dashboard Service Module
Business logic for dashboard data calculations and aggregations.
Follows the plan.md specifications and SOLID principles.
"""
from decimal import Decimal
from typing import Dict, List, Any

from utils.formatters import format_percentage, format_currency
from utils.date_utils import get_current_year


class DashboardService:
    """
    Service for dashboard business logic.
    Handles KPI calculations, trend analysis, and data aggregations.
    """

    def __init__(self, repository):
        """
        Initialize service with repository dependency injection.

        Args:
            repository: DashboardRepository instance
        """
        self.repository = repository

    def calculate_kpi_metrics(self) -> Dict[str, Any]:
        """
        Calculate KPI metrics from raw data.

        Returns:
            dict: {
                'total_performance': float (avg employment rate),
                'publication_count': int,
                'student_count': int,
                'budget_status': {
                    'total': int,
                    'executed': int,
                    'rate': float (percentage)
                }
            }
        """
        # Get latest KPI data
        kpi_data = self.repository.get_latest_kpi_data()

        # Calculate average employment rate
        if kpi_data.exists():
            total_employment_rate = sum(
                float(item.employment_rate) if item.employment_rate else 0
                for item in kpi_data
            )
            count = kpi_data.count()
            avg_employment_rate = total_employment_rate / count if count > 0 else 0.0
        else:
            avg_employment_rate = 0.0

        # Get publication count for current year
        publication_count = self.repository.get_publication_count_current_year()

        # Get active student count
        student_count = self.repository.get_active_student_count()

        # Get budget data and calculate execution rate
        budget_summary = self.repository.get_budget_summary()
        total_budget = budget_summary['total_budget']
        executed_amount = budget_summary['executed_amount']

        # Calculate execution rate (avoid division by zero)
        if total_budget > 0:
            execution_rate = (executed_amount / total_budget) * 100
        else:
            execution_rate = 0.0

        return {
            'total_performance': round(avg_employment_rate, 2),
            'publication_count': publication_count,
            'student_count': student_count,
            'budget_status': {
                'total': total_budget,
                'executed': executed_amount,
                'rate': round(execution_rate, 2)
            }
        }

    def calculate_trend_data(self) -> List[Dict[str, Any]]:
        """
        Calculate yearly trend data for the last 4 years.

        Returns:
            list: [
                {'year': int, 'value': float},
                ...
            ]
        """
        # Get yearly trends from repository (last 4 years)
        trends = self.repository.get_yearly_trends()

        # Transform into list of dicts
        result = []
        for trend in trends:
            year = trend['year']
            avg_rate = trend['avg_employment_rate']

            # Use average employment rate as the trend value
            # Handle None values
            value = float(avg_rate) if avg_rate is not None else 0.0

            result.append({
                'year': year,
                'value': round(value, 2)
            })

        return result

    def calculate_department_performance(self) -> List[Dict[str, Any]]:
        """
        Calculate department performance metrics.

        Returns:
            list: [
                {'department': str, 'value': float},
                ...
            ]
        """
        # Get department performance from repository
        performance_data = self.repository.get_department_performance()

        # Transform into list of dicts
        result = []
        for item in performance_data:
            department = item['department']
            avg_rate = item['avg_employment_rate']

            # Use average employment rate as performance value
            # Handle None values
            value = float(avg_rate) if avg_rate is not None else 0.0

            result.append({
                'department': department,
                'value': round(value, 2)
            })

        # Return top 10 departments
        return result[:10]

    def calculate_budget_allocation(self) -> List[Dict[str, Any]]:
        """
        Calculate budget allocation by department.

        Returns:
            list: [
                {'category': str, 'value': int},
                ...
            ]
        """
        # Get budget allocation from repository
        allocation_data = self.repository.get_budget_allocation()

        # Transform into list of dicts
        result = []
        for item in allocation_data:
            department = item['department']
            total_budget = item['total_budget']

            # Use department as category and total_budget as value
            # Handle None values
            value = int(total_budget) if total_budget is not None else 0

            result.append({
                'category': department,
                'value': value
            })

        # Return top 8 departments for better pie chart visualization
        return result[:8]


class PerformanceService:
    """
    Service for performance analysis business logic.
    Handles achievement rate calculations and data aggregations.
    """

    def __init__(self, repository):
        """
        Initialize service with repository dependency injection.

        Args:
            repository: PerformanceRepository instance
        """
        self.repository = repository

    def calculate_achievement_rate(self, actual, target):
        """
        Calculate achievement rate and determine status.

        Business Rule BR-3:
        - Rate = (actual / target) * 100
        - Status: >= 100 = success, >= 80 = warning, < 80 = danger

        Args:
            actual (Decimal/float): Actual performance value
            target (Decimal/float): Target performance value

        Returns:
            dict: {
                'actual': float,
                'target': float,
                'rate': float or None,
                'status': str ('success', 'warning', 'danger', 'unknown')
            }
        """
        # Handle None or zero target
        if not target or target == 0:
            return {
                'actual': float(actual) if actual else 0.0,
                'target': float(target) if target else 0.0,
                'rate': None,
                'status': 'unknown'
            }

        # Calculate rate
        rate = (float(actual) / float(target)) * 100

        # Determine status based on rate
        if rate >= 100:
            status = 'success'
        elif rate >= 80:
            status = 'warning'
        else:
            status = 'danger'

        return {
            'actual': float(actual),
            'target': float(target),
            'rate': round(rate, 2),
            'status': status
        }

    def aggregate_trend_data(self, raw_data, interval='month'):
        """
        Aggregate performance data by time interval.

        Business Rule BR-4:
        - Monthly aggregation by default
        - Sum values within each period

        Args:
            raw_data (list): Raw trend data points
            interval (str): Time interval ('month' or 'year')

        Returns:
            list: Aggregated trend data
        """
        # Since we're already grouping by year in repository,
        # just return the data as-is for now
        return raw_data

    def calculate_department_percentages(self, department_data):
        """
        Calculate percentage contribution of each department.

        Args:
            department_data (list): Department performance data

        Returns:
            list: Department data with percentage calculations
        """
        # Calculate total
        total = sum(item.get('value', 0) for item in department_data)

        if total == 0:
            return department_data

        # Add percentage to each item
        result = []
        for item in department_data:
            value = item.get('value', 0)
            percentage = (value / total) * 100 if total > 0 else 0.0

            result.append({
                **item,
                'percentage': round(percentage, 2)
            })

        return result


class PapersAnalyticsService:
    """
    Service for papers analytics business logic.
    Handles publication data aggregation and validation.
    """

    def __init__(self, repository):
        """
        Initialize service with repository dependency injection.

        Args:
            repository: PapersAnalyticsRepository instance
        """
        self.repository = repository

    def get_analytics(self, year=None, journal_grade=None, field=None) -> Dict[str, Any]:
        """
        Get complete papers analytics data.

        Args:
            year (int, optional): Filter by year
            journal_grade (str, optional): Filter by journal grade
            field (str, optional): Filter by field/department

        Returns:
            dict: {
                'yearly_data': [...],
                'journal_data': [...],
                'field_data': [...]
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
            'yearly_data': yearly_data,
            'journal_data': journal_data,
            'field_data': field_data
        }

    def validate_filters(self, year, journal_grade, field) -> bool:
        """
        Validate filter parameters.

        Business Rules:
        - Year must be between 2000 and 2100
        - Journal grade must be valid value or None
        - Field can be any string

        Args:
            year (int, optional): Year filter
            journal_grade (str, optional): Journal grade filter
            field (str, optional): Field filter

        Returns:
            bool: True if valid, False otherwise
        """
        # Validate year range
        if year is not None and (year < 2000 or year > 2100):
            return False

        # Validate journal grade
        valid_grades = ['SCI', 'KCI', 'SCOPUS', '기타', None]
        if journal_grade is not None and journal_grade not in valid_grades:
            return False

        return True


class BudgetAnalysisService:
    """
    Domain service for budget analysis business logic.

    Responsibilities:
    - Calculate budget allocation percentages
    - Calculate execution rates
    - Determine execution status (normal/warning/critical)
    - Calculate remaining budgets
    - Aggregate yearly trends
    """

    def __init__(self, repository):
        """
        Initialize service with repository dependency injection.

        Args:
            repository: BudgetRepository instance
        """
        self.repository = repository

    def calculate_budget_allocation(self, department=None, year=None, category=None):
        """
        Calculate department-wise budget allocation with percentages.

        Business Rules:
        - BR-7: Amounts formatted with thousand separators
        - Percentage calculated as (dept_budget / total_budget) * 100
        - Rounded to 2 decimal places

        Args:
            department (str, optional): Filter by department
            year (int, optional): Filter by year
            category (str, optional): Filter by category

        Returns:
            list: Budget allocation items with percentages
        """
        from datetime import datetime

        # Get raw data from repository
        budget_data = self.repository.get_budget_by_department(
            department=department,
            year=year or datetime.now().year,
            category=category
        )

        # Calculate total budget
        total_budget = sum(item['total_budget'] for item in budget_data if item['total_budget'])

        # Calculate percentages
        result = []
        for item in budget_data:
            budget = item['total_budget'] or 0
            percentage = (budget / total_budget * 100) if total_budget > 0 else 0
            result.append({
                'department': item['department'],
                'total_budget': budget,
                'percentage': round(Decimal(str(percentage)), 2),
                'project_count': item['project_count']
            })

        # Sort by budget descending
        result.sort(key=lambda x: x['total_budget'], reverse=True)

        return result

    def calculate_execution_status(self, department=None, year=None, start_date=None, end_date=None):
        """
        Calculate budget execution status with rates and warnings.

        Business Rules:
        - BR-2: Execution rate = (executed / total) * 100
        - BR-3: Remaining = total - executed
        - BR-4: Status levels:
          - normal: < 90%
          - warning: 90-100%
          - critical: > 100%

        Args:
            department (str, optional): Filter by department
            year (int, optional): Filter by year
            start_date (date, optional): Start date for filtering
            end_date (date, optional): End date for filtering

        Returns:
            list: Execution status items
        """
        from datetime import datetime

        # Get execution data
        execution_data = self.repository.get_execution_by_department(
            department=department,
            year=year or datetime.now().year,
            start_date=start_date,
            end_date=end_date
        )

        result = []
        for item in execution_data:
            total = item['total_budget'] or 0
            executed = item['executed_amount'] or 0

            # Calculate execution rate (BR-2)
            rate = (executed / total * 100) if total > 0 else 0

            # Calculate remaining (BR-3)
            remaining = total - executed

            # Determine status (BR-4)
            if rate >= 100:
                status = 'critical'
            elif rate >= 90:
                status = 'warning'
            else:
                status = 'normal'

            result.append({
                'department': item['department'],
                'total_budget': total,
                'executed_amount': executed,
                'execution_rate': round(Decimal(str(rate)), 2),
                'remaining_budget': remaining,
                'status': status
            })

        return result

    def calculate_execution_summary(self, execution_data):
        """
        Calculate overall execution summary.

        Args:
            execution_data (list): List of execution status items

        Returns:
            dict: Summary with total_budget, total_executed, overall_rate
        """
        total_budget = sum(item['total_budget'] for item in execution_data)
        total_executed = sum(item['executed_amount'] for item in execution_data)
        overall_rate = (total_executed / total_budget * 100) if total_budget > 0 else 0

        return {
            'total_budget': total_budget,
            'total_executed': total_executed,
            'overall_rate': round(Decimal(str(overall_rate)), 2)
        }

    def calculate_yearly_trends(self, department=None, start_year=None, end_year=None):
        """
        Calculate year-over-year budget trends.

        Args:
            department (str, optional): Filter by department
            start_year (int, optional): Start year for trends
            end_year (int, optional): End year for trends

        Returns:
            list: Yearly trend items
        """
        trends_data = self.repository.get_yearly_trends(
            department=department,
            start_year=start_year,
            end_year=end_year
        )

        result = []
        for item in trends_data:
            total_budget = item['total_budget'] or 0
            executed_amount = item['executed_amount'] or 0
            rate = (executed_amount / total_budget * 100) if total_budget > 0 else 0

            result.append({
                'year': item['year'],
                'total_budget': total_budget,
                'executed_amount': executed_amount,
                'execution_rate': round(Decimal(str(rate)), 2)
            })

        # Sort by year ascending
        result.sort(key=lambda x: x['year'])

        return result


class FileValidationService:
    """
    Service for file validation business logic.
    Validates uploaded files before processing.
    Pure business logic - no persistence logic.
    """

    ALLOWED_EXTENSIONS = ['.xlsx', '.xls', '.csv']
    MAX_FILE_SIZE_MB = 10

    def validate_file_format(self, filename: str) -> bool:
        """
        Validate file extension.

        Args:
            filename: Name of the file

        Returns:
            bool: True if valid format

        Raises:
            ValueError: If invalid format
        """
        import os

        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Invalid file format. Only {', '.join(self.ALLOWED_EXTENSIONS)} files are allowed."
            )

        return True

    def validate_file_size(self, file_size: int, max_size_mb: int = None) -> bool:
        """
        Validate file size is within limit.

        Args:
            file_size: File size in bytes
            max_size_mb: Maximum size in MB (default: 10MB)

        Returns:
            bool: True if size is valid

        Raises:
            ValueError: If file size exceeds limit
        """
        if max_size_mb is None:
            max_size_mb = self.MAX_FILE_SIZE_MB

        max_bytes = max_size_mb * 1024 * 1024

        if file_size > max_bytes:
            raise ValueError(
                f"File size exceeds {max_size_mb}MB limit. File size: {file_size / (1024 * 1024):.2f}MB"
            )

        return True

    def detect_file_type(self, filename: str, columns: List[str]) -> str:
        """
        Detect which data type the file contains based on columns.

        Args:
            filename: Name of the file
            columns: List of column names from file

        Returns:
            str: File type ('department_kpi', 'publication_list',
                 'student_roster', 'research_project_data')

        Raises:
            ValueError: If file type cannot be determined
        """
        from ..infrastructure.file_parsers import ParserFactory

        try:
            file_type = ParserFactory.detect_file_type(columns)
            return file_type
        except Exception as e:
            raise ValueError(f"Could not detect file type: {str(e)}")

    def validate_business_rules(self, file_type: str, data: List[Dict]) -> List[Dict]:
        """
        Apply business rule validations.

        Business Rules:
        - BR-4: Data Validation (required fields, data types)
        - Check year ranges (2000-2100)
        - Check valid enum values

        Args:
            file_type: Type of data file
            data: List of dictionaries with data

        Returns:
            List of validation errors (empty if all valid)
        """
        errors = []

        for idx, row in enumerate(data):
            row_num = idx + 2  # +2 for Excel (1-indexed + header row)

            # Validate year range (if year field exists)
            if 'year' in row and row['year'] is not None:
                year = row['year']
                if not isinstance(year, int) or year < 2000 or year > 2100:
                    errors.append({
                        'row': row_num,
                        'column': 'year',
                        'message': f"Year must be between 2000 and 2100. Got: {year}",
                        'severity': 'error'
                    })

            # Validate enrollment_status for students
            if file_type == 'student_roster' and 'enrollment_status' in row:
                valid_statuses = ['재학', '휴학', '졸업', '자퇴', '제적']
                status = row['enrollment_status']
                if status and status not in valid_statuses:
                    errors.append({
                        'row': row_num,
                        'column': 'enrollment_status',
                        'message': f"Invalid enrollment status. Must be one of: {', '.join(valid_statuses)}",
                        'severity': 'error'
                    })

            # Validate budget status
            if file_type == 'research_project_data' and 'status' in row:
                valid_statuses = ['집행완료', '처리중', '취소']
                status = row['status']
                if status and status not in valid_statuses:
                    errors.append({
                        'row': row_num,
                        'column': 'status',
                        'message': f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
                        'severity': 'error'
                    })

        return errors


class DataProcessingService:
    """
    Service for data processing business logic.
    Processes parsed data according to business rules.
    Coordinates between parser and repository.
    """

    def __init__(self, repository):
        """
        Initialize service with repository dependency injection.

        Args:
            repository: DataUploadRepository instance
        """
        self.repository = repository

    def process_department_kpi(self, data: List[Dict]) -> Dict:
        """
        Process department KPI data.

        Args:
            data: List of dictionaries with KPI data

        Returns:
            dict: {'records_processed': int, 'duplicates_found': int}
        """
        from ..models import DepartmentKPI

        unique_fields = ['year', 'college', 'department']

        # Count existing records before upsert
        existing_count = self.repository.count_records(
            DepartmentKPI,
            {'year': data[0]['year']} if data else {}
        )

        # Bulk upsert
        records_processed = self.repository.bulk_upsert(
            DepartmentKPI,
            data,
            unique_fields
        )

        # Calculate duplicates (records that were updated)
        duplicates_found = min(existing_count, records_processed)

        return {
            'records_processed': records_processed,
            'duplicates_found': duplicates_found
        }

    def process_publication(self, data: List[Dict]) -> Dict:
        """
        Process publication data.

        Args:
            data: List of dictionaries with publication data

        Returns:
            dict: {'records_processed': int, 'duplicates_found': int}
        """
        from ..models import Publication

        unique_fields = ['publication_id']

        # Count existing publications
        existing_count = len([
            d for d in data
            if Publication.objects.filter(publication_id=d.get('publication_id')).exists()
        ])

        # Bulk upsert
        records_processed = self.repository.bulk_upsert(
            Publication,
            data,
            unique_fields
        )

        return {
            'records_processed': records_processed,
            'duplicates_found': existing_count
        }

    def process_student(self, data: List[Dict]) -> Dict:
        """
        Process student data.

        Args:
            data: List of dictionaries with student data

        Returns:
            dict: {'records_processed': int, 'duplicates_found': int}
        """
        from ..models import Student

        unique_fields = ['student_id']

        # Count existing students
        existing_count = len([
            d for d in data
            if Student.objects.filter(student_id=d.get('student_id')).exists()
        ])

        # Bulk upsert
        records_processed = self.repository.bulk_upsert(
            Student,
            data,
            unique_fields
        )

        return {
            'records_processed': records_processed,
            'duplicates_found': existing_count
        }

    def process_research_budget(self, data: List[Dict]) -> Dict:
        """
        Process research budget data.

        Args:
            data: List of dictionaries with research budget data

        Returns:
            dict: {'records_processed': int, 'duplicates_found': int}
        """
        from ..models import ResearchBudgetData

        unique_fields = ['execution_id']

        # Count existing executions
        existing_count = len([
            d for d in data
            if ResearchBudgetData.objects.filter(execution_id=d.get('execution_id')).exists()
        ])

        # Bulk upsert
        records_processed = self.repository.bulk_upsert(
            ResearchBudgetData,
            data,
            unique_fields
        )

        return {
            'records_processed': records_processed,
            'duplicates_found': existing_count
        }
