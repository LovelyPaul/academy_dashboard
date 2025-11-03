"""
Dashboard Serializers Module
Presentation layer serializers for dashboard API responses.
Follows plan.md specifications for data structure.
"""
from rest_framework import serializers


class BudgetStatusSerializer(serializers.Serializer):
    """
    Serializer for budget status data.
    """
    total = serializers.IntegerField(
        help_text="Total budget amount (KRW)"
    )
    executed = serializers.IntegerField(
        help_text="Executed budget amount (KRW)"
    )
    rate = serializers.FloatField(
        help_text="Execution rate (percentage)"
    )


class KPIDataSerializer(serializers.Serializer):
    """
    Serializer for KPI metrics data.
    """
    total_performance = serializers.FloatField(
        help_text="Average employment rate (%)"
    )
    publication_count = serializers.IntegerField(
        help_text="Total publication count for current year"
    )
    student_count = serializers.IntegerField(
        help_text="Active student count (재학)"
    )
    budget_status = BudgetStatusSerializer(
        help_text="Budget status information"
    )


class TrendDataItemSerializer(serializers.Serializer):
    """
    Serializer for a single trend data point.
    """
    year = serializers.IntegerField(
        help_text="Year"
    )
    value = serializers.FloatField(
        help_text="Average employment rate for the year"
    )


class DepartmentDataItemSerializer(serializers.Serializer):
    """
    Serializer for a single department performance data point.
    """
    department = serializers.CharField(
        max_length=100,
        help_text="Department name"
    )
    value = serializers.FloatField(
        help_text="Department performance value (avg employment rate)"
    )


class BudgetDataItemSerializer(serializers.Serializer):
    """
    Serializer for a single budget allocation data point.
    """
    category = serializers.CharField(
        max_length=100,
        help_text="Budget category (department name)"
    )
    value = serializers.IntegerField(
        help_text="Budget amount (KRW)"
    )


class DashboardSerializer(serializers.Serializer):
    """
    Main serializer for complete dashboard response.
    Aggregates all dashboard data into a single response.
    """
    kpi_data = KPIDataSerializer(
        help_text="KPI metrics data"
    )
    trend_data = TrendDataItemSerializer(
        many=True,
        help_text="Yearly trend data"
    )
    department_data = DepartmentDataItemSerializer(
        many=True,
        help_text="Department performance data"
    )
    budget_data = BudgetDataItemSerializer(
        many=True,
        help_text="Budget allocation data"
    )
    last_updated = serializers.DateTimeField(
        help_text="Last updated timestamp (ISO format)"
    )


# Performance Analysis Serializers

class PerformanceFilterSerializer(serializers.Serializer):
    """
    Validates incoming filter parameters for performance analysis.
    """
    start_date = serializers.DateField(
        required=False,
        help_text="Start date (YYYY-MM-DD)"
    )
    end_date = serializers.DateField(
        required=False,
        help_text="End date (YYYY-MM-DD)"
    )
    department = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=100,
        help_text="Department filter"
    )
    project = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=50,
        help_text="Project filter"
    )

    def validate(self, data):
        """
        Custom validation for date range.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError(
                    "Start date must be before end date"
                )

        return data


class TrendDataPointSerializer(serializers.Serializer):
    """
    Serializes a single trend data point.
    """
    date = serializers.CharField(
        help_text="Date (YYYY-MM-DD)"
    )
    value = serializers.FloatField(
        help_text="Performance value"
    )
    target = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text="Target value"
    )


class DepartmentDataPointSerializer(serializers.Serializer):
    """
    Serializes a single department data point.
    """
    department = serializers.CharField(
        help_text="Department name"
    )
    value = serializers.FloatField(
        help_text="Performance value"
    )
    percentage = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text="Percentage of total"
    )


class AchievementDataSerializer(serializers.Serializer):
    """
    Serializes achievement rate data.
    """
    actual = serializers.FloatField(
        help_text="Actual performance value"
    )
    target = serializers.FloatField(
        help_text="Target performance value"
    )
    rate = serializers.FloatField(
        allow_null=True,
        help_text="Achievement rate (percentage)"
    )
    status = serializers.ChoiceField(
        choices=['success', 'warning', 'danger', 'unknown'],
        help_text="Achievement status"
    )


class PerformanceResponseSerializer(serializers.Serializer):
    """
    Serializes the complete performance response.
    """
    trendData = TrendDataPointSerializer(
        many=True,
        help_text="Trend data over time"
    )
    departmentData = DepartmentDataPointSerializer(
        many=True,
        help_text="Department comparison data"
    )
    achievementData = AchievementDataSerializer(
        help_text="Achievement rate data"
    )


class YearlyDataSerializer(serializers.Serializer):
    """Serializer for yearly publication data."""
    year = serializers.IntegerField(
        help_text="Publication year"
    )
    count = serializers.IntegerField(
        help_text="Number of publications in that year"
    )


class JournalDataSerializer(serializers.Serializer):
    """Serializer for journal distribution data."""
    journal_grade = serializers.CharField(
        max_length=50,
        help_text="Journal grade (SCI, KCI, SCOPUS, etc.)"
    )
    count = serializers.IntegerField(
        help_text="Number of publications in that grade"
    )


class FieldDataSerializer(serializers.Serializer):
    """Serializer for field statistics data."""
    department = serializers.CharField(
        max_length=100,
        help_text="Department/field name"
    )
    count = serializers.IntegerField(
        help_text="Number of publications from that department"
    )


class PapersAnalyticsSerializer(serializers.Serializer):
    """Serializer for complete papers analytics response."""
    yearly_data = YearlyDataSerializer(
        many=True,
        help_text="Yearly publication counts"
    )
    journal_data = JournalDataSerializer(
        many=True,
        help_text="Journal grade distribution"
    )
    field_data = FieldDataSerializer(
        many=True,
        help_text="Field-wise publication statistics"
    )
    has_data = serializers.BooleanField(
        help_text="Whether any data exists"
    )


# Budget Analysis Serializers

class BudgetFilterSerializer(serializers.Serializer):
    """Validates query parameters for budget endpoints"""

    department = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=100,
        help_text="Filter by department"
    )
    year = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=2000,
        max_value=2100,
        help_text="Filter by year (default: current year)"
    )
    category = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        max_length=100,
        help_text="Filter by budget category"
    )
    start_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Start date for execution filter"
    )
    end_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="End date for execution filter"
    )
    start_year = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=2000,
        max_value=2100,
        help_text="Start year for trends"
    )
    end_year = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=2000,
        max_value=2100,
        help_text="End year for trends"
    )

    def validate(self, data):
        """Cross-field validation"""
        # Validate date range
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    "start_date must be before end_date"
                )

        # Validate year range
        if data.get('start_year') and data.get('end_year'):
            if data['start_year'] > data['end_year']:
                raise serializers.ValidationError(
                    "start_year must be before end_year"
                )

        return data


class BudgetAllocationSerializer(serializers.Serializer):
    """Serializes budget allocation data"""

    department = serializers.CharField(
        max_length=100,
        help_text="Department name"
    )
    total_budget = serializers.IntegerField(
        help_text="Total budget amount (KRW)"
    )
    percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage of overall budget"
    )
    project_count = serializers.IntegerField(
        help_text="Number of projects in department"
    )


class ExecutionStatusSerializer(serializers.Serializer):
    """Serializes budget execution status"""

    department = serializers.CharField(
        max_length=100,
        help_text="Department name"
    )
    total_budget = serializers.IntegerField(
        help_text="Total budget amount (KRW)"
    )
    executed_amount = serializers.IntegerField(
        help_text="Executed budget amount (KRW)"
    )
    execution_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Execution rate (%)"
    )
    remaining_budget = serializers.IntegerField(
        help_text="Remaining budget amount (KRW)"
    )
    status = serializers.ChoiceField(
        choices=['normal', 'warning', 'critical'],
        help_text="Execution status (normal: <90%, warning: 90-100%, critical: >100%)"
    )


class ExecutionSummarySerializer(serializers.Serializer):
    """Serializes execution summary data"""

    total_budget = serializers.IntegerField(
        help_text="Total budget across all departments (KRW)"
    )
    total_executed = serializers.IntegerField(
        help_text="Total executed amount across all departments (KRW)"
    )
    overall_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Overall execution rate (%)"
    )


class YearlyTrendsSerializer(serializers.Serializer):
    """Serializes yearly budget trends"""

    year = serializers.IntegerField(
        help_text="Year"
    )
    total_budget = serializers.IntegerField(
        help_text="Total budget for the year (KRW)"
    )
    executed_amount = serializers.IntegerField(
        help_text="Executed amount for the year (KRW)"
    )
    execution_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Execution rate for the year (%)"
    )


# Upload Serializers

class UploadFileSerializer(serializers.Serializer):
    """
    Serializer for file upload validation.
    Validates file format and size on API level.
    """
    file = serializers.FileField(
        required=True,
        allow_empty_file=False,
        help_text="Excel or CSV file (.xlsx, .xls, or .csv), max 10MB"
    )

    def validate_file(self, value):
        """
        Validate file extension and size.

        Args:
            value: Uploaded file

        Returns:
            Validated file

        Raises:
            ValidationError: If file is invalid
        """
        # Check extension
        if not value.name.endswith(('.xlsx', '.xls', '.csv')):
            raise serializers.ValidationError(
                "Invalid file format. Only .xlsx, .xls, and .csv files are allowed."
            )

        # Check size (10MB = 10 * 1024 * 1024 bytes)
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File size exceeds 10MB limit. Current size: {value.size / (1024 * 1024):.2f}MB"
            )

        return value


class ValidationErrorSerializer(serializers.Serializer):
    """
    Serializer for validation error details.
    """
    row = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Row number where error occurred"
    )
    column = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="Column name where error occurred"
    )
    message = serializers.CharField(
        help_text="Error message"
    )
    severity = serializers.ChoiceField(
        choices=['error', 'warning'],
        help_text="Error severity level"
    )


class UploadResultSerializer(serializers.Serializer):
    """
    Serializer for upload result response.
    """
    success = serializers.BooleanField(
        help_text="Whether upload was successful"
    )
    records_processed = serializers.IntegerField(
        help_text="Number of records processed"
    )
    file_type = serializers.CharField(
        help_text="Detected file type"
    )
    file_name = serializers.CharField(
        help_text="Original file name"
    )
    duplicates_found = serializers.IntegerField(
        required=False,
        help_text="Number of duplicate records found"
    )
    errors = ValidationErrorSerializer(
        many=True,
        required=False,
        help_text="List of validation errors (if any)"
    )


class UploadHistorySerializer(serializers.Serializer):
    """
    Serializer for upload history records.
    """
    id = serializers.IntegerField(
        read_only=True,
        help_text="History record ID"
    )
    file_name = serializers.CharField(
        help_text="Original file name"
    )
    file_type = serializers.ChoiceField(
        choices=[
            ('department_kpi', 'Department KPI'),
            ('publication_list', 'Publication List'),
            ('research_project_data', 'Research Project Data'),
            ('student_roster', 'Student Roster'),
        ],
        help_text="Type of data file"
    )
    status = serializers.ChoiceField(
        choices=[
            ('success', 'Success'),
            ('failed', 'Failed'),
        ],
        help_text="Upload status"
    )
    records_processed = serializers.IntegerField(
        help_text="Number of records processed"
    )
    error_message = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="Error message if upload failed"
    )
    uploaded_at = serializers.DateTimeField(
        help_text="Upload timestamp"
    )
    uploaded_by = serializers.CharField(
        help_text="Email of user who uploaded"
    )


class UploadHistoryListSerializer(serializers.Serializer):
    """
    Serializer for paginated upload history list.
    """
    results = UploadHistorySerializer(
        many=True,
        help_text="List of upload history records"
    )
    total = serializers.IntegerField(
        help_text="Total number of records"
    )
    page = serializers.IntegerField(
        help_text="Current page number"
    )
    page_size = serializers.IntegerField(
        help_text="Number of records per page"
    )
