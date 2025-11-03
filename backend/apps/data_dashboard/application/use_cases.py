"""
Dashboard Use Cases Module
Application layer for orchestrating dashboard workflows.
Implements the GetDashboardDataUseCase following plan.md specifications.
"""
from datetime import datetime
from typing import Dict, Any

from core.exceptions import NotFoundError, ValidationError


class GetDashboardDataUseCase:
    """
    Use case for fetching complete dashboard data.
    Orchestrates service calls and handles errors.
    """

    def __init__(self, service):
        """
        Initialize use case with service dependency injection.

        Args:
            service: DashboardService instance
        """
        self.service = service

    def execute(self) -> Dict[str, Any]:
        """
        Execute dashboard data retrieval workflow.

        Returns:
            dict: Complete dashboard data including:
                - kpi_data: KPI metrics
                - trend_data: Yearly trends
                - department_data: Department performance
                - budget_data: Budget allocation
                - last_updated: ISO timestamp

        Raises:
            NotFoundError: If no data exists
            ValidationError: If data is invalid
        """
        try:
            # Step 1: Calculate KPI metrics
            kpi_data = self.service.calculate_kpi_metrics()

            # Step 2: Calculate trend data
            trend_data = self.service.calculate_trend_data()

            # Step 3: Calculate department performance
            department_data = self.service.calculate_department_performance()

            # Step 4: Calculate budget allocation
            budget_data = self.service.calculate_budget_allocation()

            # Step 5: Validate that we have at least some data
            if not kpi_data or not trend_data:
                raise NotFoundError("Dashboard data is empty. Please upload data first.")

            # Step 6: Return aggregated data
            return {
                'kpi_data': kpi_data,
                'trend_data': trend_data,
                'department_data': department_data,
                'budget_data': budget_data,
                'last_updated': datetime.now().isoformat()
            }

        except NotFoundError:
            # Re-raise NotFoundError as is
            raise

        except ValidationError:
            # Re-raise ValidationError as is
            raise

        except Exception as e:
            # Log the error and raise a generic server error
            # In production, you would log this properly
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching dashboard data: {str(e)}", exc_info=True)

            raise Exception(f"Failed to fetch dashboard data: {str(e)}")


class GetPerformanceDataUseCase:
    """
    Use case: Retrieve performance analysis data.

    Orchestrates:
    1. Filter validation
    2. Data retrieval from repository
    3. Business logic application via service
    4. Response formatting
    """

    def __init__(self, repository, service):
        """
        Initialize use case with dependencies.

        Args:
            repository: PerformanceRepository instance
            service: PerformanceService instance
        """
        self.repository = repository
        self.service = service

    def execute(self, start_date, end_date, department=None, project=None):
        """
        Execute the performance data retrieval use case.

        Args:
            start_date (date): Start date for filtering
            end_date (date): End date for filtering
            department (str, optional): Department filter
            project (str, optional): Project filter

        Returns:
            dict: {
                'trendData': list of trend data points,
                'departmentData': list of department comparisons,
                'achievementData': achievement rate data
            }

        Raises:
            ValidationError: If filters are invalid
        """
        # 1. Validate filters (BR-2)
        self._validate_date_range(start_date, end_date)

        # 2. Fetch raw data from repository
        trend_data = self.repository.get_performance_trend(
            start_date, end_date, department, project
        )

        department_data = self.repository.get_department_comparison(
            start_date, end_date, project
        )

        achievement_raw = self.repository.get_achievement_rate(
            start_date, end_date, department
        )

        # 3. Apply business logic via service
        trend_aggregated = self.service.aggregate_trend_data(trend_data)
        dept_with_percentages = self.service.calculate_department_percentages(
            department_data
        )
        achievement_calculated = self.service.calculate_achievement_rate(
            achievement_raw['actual'],
            achievement_raw['target']
        )

        # 4. Return formatted response
        return {
            'trendData': trend_aggregated,
            'departmentData': dept_with_percentages,
            'achievementData': achievement_calculated
        }

    def _validate_date_range(self, start_date, end_date):
        """
        Validate date range according to BR-2.

        Args:
            start_date (date): Start date
            end_date (date): End date

        Raises:
            ValidationError: If date range is invalid
        """
        if start_date > end_date:
            raise ValidationError("Start date must be before end date")

        # Calculate year difference
        year_diff = (end_date - start_date).days / 365.25

        # Maximum query period is 5 years
        if year_diff > 5:
            raise ValidationError("Maximum query period is 5 years")


class GetPapersAnalyticsUseCase:
    """
    Use case for retrieving papers analytics data.
    Orchestrates papers analytics workflow with filtering.
    """

    def __init__(self):
        """
        Initialize use case with repository and service.
        Uses dependency injection pattern.
        """
        from ..infrastructure.repositories import PapersAnalyticsRepository
        from ..domain.services import PapersAnalyticsService

        self.repository = PapersAnalyticsRepository()
        self.service = PapersAnalyticsService(self.repository)

    def execute(self, year=None, journal_grade=None, field=None) -> Dict[str, Any]:
        """
        Execute the papers analytics use case.

        Args:
            year (int, optional): Filter by year
            journal_grade (str, optional): Filter by journal grade
            field (str, optional): Filter by field/department

        Returns:
            dict: {
                'yearly_data': list of yearly counts,
                'journal_data': list of journal distribution,
                'field_data': list of field statistics,
                'has_data': bool indicating if any data exists
            }

        Raises:
            ValidationError: If filters are invalid
        """
        # Validate filters
        if not self.service.validate_filters(year, journal_grade, field):
            raise ValidationError("Invalid filter parameters")

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
            'has_data': has_data
        }


class BudgetAnalysisUseCase:
    """
    Use case for budget analysis operations.

    Orchestrates the interaction between service layer and repository
    to provide budget analysis data for the presentation layer.
    """

    def __init__(self):
        """
        Initialize use case with repository and service.
        Uses dependency injection pattern.
        """
        from ..infrastructure.repositories import BudgetRepository
        from ..domain.services import BudgetAnalysisService

        self.repository = BudgetRepository()
        self.service = BudgetAnalysisService(self.repository)

    def get_budget_allocation(self, department=None, year=None, category=None):
        """
        Get department-wise budget allocation.

        Args:
            department (str, optional): Filter by specific department
            year (int, optional): Filter by year (default: current year)
            category (str, optional): Filter by budget category

        Returns:
            list: List of budget allocation items with:
                - department: Department name
                - total_budget: Total budget amount
                - percentage: Percentage of overall budget
                - project_count: Number of projects

        Raises:
            ValidationError: If filters are invalid
            NotFoundError: If no data found
        """
        # Delegate to service layer
        result = self.service.calculate_budget_allocation(
            department=department,
            year=year,
            category=category
        )

        # Return empty list if no data found (consistent with other endpoints)
        return result if result else []

    def get_execution_status(self, department=None, year=None, start_date=None, end_date=None):
        """
        Get budget execution status with rates and warnings.

        Args:
            department (str, optional): Filter by department
            year (int, optional): Filter by year
            start_date (date, optional): Start date for execution period
            end_date (date, optional): End date for execution period

        Returns:
            dict: Dictionary with:
                - data: List of execution status items
                - summary: Overall execution summary

        Raises:
            ValidationError: If date range is invalid
        """
        # Validate date range
        if start_date and end_date and start_date > end_date:
            raise ValidationError("start_date must be before end_date")

        # Get execution data from service
        data = self.service.calculate_execution_status(
            department=department,
            year=year,
            start_date=start_date,
            end_date=end_date
        )

        # Calculate summary
        summary = self.service.calculate_execution_summary(data)

        return {
            'data': data,
            'summary': summary
        }

    def get_yearly_trends(self, department=None, start_year=None, end_year=None):
        """
        Get year-over-year budget trends.

        Args:
            department (str, optional): Filter by department
            start_year (int, optional): Start year for trend analysis
            end_year (int, optional): End year for trend analysis

        Returns:
            list: List of yearly trend items

        Raises:
            ValidationError: If year range is invalid
        """
        # Validate year range
        if start_year and end_year and start_year > end_year:
            raise ValidationError("start_year must be before end_year")

        result = self.service.calculate_yearly_trends(
            department=department,
            start_year=start_year,
            end_year=end_year
        )

        return result


class UploadFileUseCase:
    """
    Use case for file upload workflow.
    Orchestrates the complete upload process from validation to database save.
    Follows SRP: Only coordinates the upload flow.
    """

    def __init__(self):
        """
        Initialize use case with all required dependencies.
        """
        from ..domain.services import FileValidationService, DataProcessingService
        from ..infrastructure.repositories import DataUploadRepository, UploadHistoryRepository
        from ..infrastructure.file_parsers import ParserFactory, ExcelParser
        import tempfile
        import os

        self.validation_service = FileValidationService()
        self.upload_repo = DataUploadRepository()
        self.processing_service = DataProcessingService(self.upload_repo)
        self.history_repository = UploadHistoryRepository()
        self.parser_factory = ParserFactory
        self.ExcelParser = ExcelParser  # Store class reference
        self.temp_dir = tempfile.gettempdir()

    def execute(self, user_id: int, uploaded_file) -> Dict:
        """
        Execute upload workflow:
        1. Validate file format and size
        2. Save file temporarily
        3. Parse file
        4. Detect file type
        5. Validate data
        6. Process and save data
        7. Record upload history
        8. Return result

        Args:
            user_id: ID of user uploading the file
            uploaded_file: Django UploadedFile object

        Returns:
            dict: {
                'success': bool,
                'records_processed': int,
                'file_type': str,
                'file_name': str,
                'errors': List[Dict] (if validation fails)
            }

        Raises:
            ValidationError: If validation fails
            FileProcessingError: If processing fails
        """
        import os
        import logging

        logger = logging.getLogger(__name__)
        temp_file_path = None

        try:
            # Step 1: Validate file format and size
            logger.info(f"Validating file: {uploaded_file.name}")
            self.validation_service.validate_file_format(uploaded_file.name)
            self.validation_service.validate_file_size(uploaded_file.size)

            # Step 2: Save file temporarily
            temp_file_path = self._save_temp_file(uploaded_file)
            logger.info(f"Saved temporary file: {temp_file_path}")

            # Step 3: Parse file to get DataFrame
            parser = self.ExcelParser()
            df = parser.parse(temp_file_path)

            if df.empty:
                raise ValidationError("File contains no data")

            # Step 4: Detect file type based on columns
            columns = df.columns.tolist()
            file_type = self.validation_service.detect_file_type(
                uploaded_file.name,
                columns
            )
            logger.info(f"Detected file type: {file_type}")

            # Step 5: Parse file to dict using appropriate parser
            specific_parser = self.parser_factory.get_parser(file_type)
            data = specific_parser.parse_to_dict(temp_file_path)

            # Step 6: Validate business rules
            validation_errors = self.validation_service.validate_business_rules(
                file_type,
                data
            )

            if validation_errors:
                # Record failed upload in history
                self.history_repository.create_history(
                    user_id=user_id,
                    file_name=uploaded_file.name,
                    file_type=file_type,
                    status='failed',
                    records_processed=0,
                    error_message=f"{len(validation_errors)} validation errors found"
                )

                return {
                    'success': False,
                    'file_name': uploaded_file.name,
                    'file_type': file_type,
                    'records_processed': 0,
                    'errors': validation_errors
                }

            # Step 7: Process and save data based on file type
            if file_type == 'department_kpi':
                result = self.processing_service.process_department_kpi(data)
            elif file_type == 'publication_list':
                result = self.processing_service.process_publication(data)
            elif file_type == 'student_roster':
                result = self.processing_service.process_student(data)
            elif file_type == 'research_project_data':
                result = self.processing_service.process_research_budget(data)
            else:
                raise ValidationError(f"Unsupported file type: {file_type}")

            records_processed = result['records_processed']
            logger.info(f"Processed {records_processed} records")

            # Step 8: Record successful upload in history
            self.history_repository.create_history(
                user_id=user_id,
                file_name=uploaded_file.name,
                file_type=file_type,
                status='success',
                records_processed=records_processed,
                error_message=None
            )

            # Step 9: Return success result
            return {
                'success': True,
                'records_processed': records_processed,
                'file_type': file_type,
                'file_name': uploaded_file.name,
                'duplicates_found': result.get('duplicates_found', 0),
                'errors': []
            }

        except (ValueError, ValidationError) as e:
            logger.error(f"Validation error: {str(e)}")

            # Record failed upload
            try:
                self.history_repository.create_history(
                    user_id=user_id,
                    file_name=uploaded_file.name,
                    file_type='unknown',
                    status='failed',
                    records_processed=0,
                    error_message=str(e)
                )
            except Exception:
                pass  # Don't fail if history recording fails

            raise ValidationError(str(e))

        except Exception as e:
            logger.error(f"Upload error: {str(e)}", exc_info=True)

            # Record failed upload
            try:
                self.history_repository.create_history(
                    user_id=user_id,
                    file_name=uploaded_file.name,
                    file_type='unknown',
                    status='failed',
                    records_processed=0,
                    error_message=str(e)
                )
            except Exception:
                pass

            raise Exception(f"Failed to process file: {str(e)}")

        finally:
            # Step 10: Cleanup temp file
            if temp_file_path:
                self._cleanup_temp_file(temp_file_path)

    def _save_temp_file(self, uploaded_file) -> str:
        """
        Save uploaded file to temp storage.

        Args:
            uploaded_file: Django UploadedFile object

        Returns:
            str: Path to temp file
        """
        import os
        import uuid

        # Generate unique filename
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_filename = f"upload_{uuid.uuid4()}{file_ext}"
        temp_file_path = os.path.join(self.temp_dir, temp_filename)

        # Write file to disk
        with open(temp_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return temp_file_path

    def _cleanup_temp_file(self, file_path: str):
        """
        Remove temp file after processing.

        Args:
            file_path: Path to temp file
        """
        import os
        import logging

        logger = logging.getLogger(__name__)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file {file_path}: {str(e)}")


class GetUploadHistoryUseCase:
    """
    Use case for retrieving upload history.
    Retrieves upload history with pagination.
    Follows SRP: Only coordinates history retrieval.
    """

    def __init__(self):
        """
        Initialize use case with repository dependency.
        """
        from ..infrastructure.repositories import UploadHistoryRepository

        self.history_repository = UploadHistoryRepository()

    def execute(self, user_id: int, page: int = 1, page_size: int = 20, is_admin: bool = False) -> Dict:
        """
        Get upload history.
        - Admin: See all uploads
        - Non-admin: See only own uploads

        Args:
            user_id: ID of requesting user
            page: Page number (1-indexed)
            page_size: Number of records per page
            is_admin: Whether user is admin

        Returns:
            dict: {
                'results': List[UploadHistory],
                'total': int,
                'page': int,
                'page_size': int
            }
        """
        # Validate pagination parameters
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 20

        # Get history based on user role
        if is_admin:
            # Admin sees all uploads
            history_records = self.history_repository.get_history_list(page, page_size)
            total = self.history_repository.get_history_count()
        else:
            # Non-admin sees only own uploads
            history_records = self.history_repository.get_history_by_user(
                user_id, page, page_size
            )
            # Get total count for user
            from ..models import UploadHistory
            total = UploadHistory.objects.filter(user_id=user_id).count()

        # Serialize history records
        results = []
        for record in history_records:
            results.append({
                'id': record.id,
                'file_name': record.file_name,
                'file_type': record.file_type,
                'status': record.status,
                'records_processed': record.records_processed,
                'error_message': record.error_message,
                'uploaded_at': record.uploaded_at.isoformat(),
                'uploaded_by': record.user.email if hasattr(record.user, 'email') else str(record.user)
            })

        return {
            'results': results,
            'total': total,
            'page': page,
            'page_size': page_size
        }
