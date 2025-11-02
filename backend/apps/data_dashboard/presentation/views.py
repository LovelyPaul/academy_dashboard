"""
Dashboard Views Module
Presentation layer API endpoints for dashboard data.
Follows plan.md specifications and layered architecture.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from backend.core.exceptions import NotFoundError, ValidationError
from ..infrastructure.repositories import DashboardRepository, PerformanceRepository
from ..domain.services import DashboardService, PerformanceService
from ..application.use_cases import GetDashboardDataUseCase, GetPerformanceDataUseCase
from .serializers import (
    DashboardSerializer,
    PerformanceFilterSerializer,
    PerformanceResponseSerializer
)
from datetime import datetime, timedelta


class DashboardViewSet(viewsets.ViewSet):
    """
    Dashboard API ViewSet.

    Provides endpoints for retrieving dashboard data.
    Authentication is handled by ClerkAuthenticationMiddleware.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/dashboard/

        Retrieve complete dashboard data including:
        - KPI metrics (총 실적, 논문 수, 학생 수, 예산 현황)
        - Trend data (yearly trends for last 4 years)
        - Department performance (top 10 departments)
        - Budget allocation (top 8 departments)

        Authentication: Required (JWT token via Bearer header)

        Response: 200 OK
        {
            "kpi_data": {
                "total_performance": 85.5,
                "publication_count": 124,
                "student_count": 1543,
                "budget_status": {
                    "total": 5000000000,
                    "executed": 3500000000,
                    "rate": 70.0
                }
            },
            "trend_data": [
                {"year": 2020, "value": 75.2},
                {"year": 2021, "value": 78.5},
                ...
            ],
            "department_data": [
                {"department": "컴퓨터공학과", "value": 92.3},
                ...
            ],
            "budget_data": [
                {"category": "인건비", "value": 2000000000},
                ...
            ],
            "last_updated": "2025-11-03T10:30:00.123456"
        }

        Error Responses:
        - 401 Unauthorized: Invalid/missing JWT token
        - 404 Not Found: No dashboard data available
        - 500 Internal Server Error: Server error
        """
        try:
            # Initialize dependencies (Dependency Injection)
            repository = DashboardRepository()
            service = DashboardService(repository)
            use_case = GetDashboardDataUseCase(service)

            # Execute use case
            data = use_case.execute()

            # Serialize response
            serializer = DashboardSerializer(data)

            # Return successful response
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except NotFoundError as e:
            # No data found
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'NOT_FOUND'
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except ValidationError as e:
            # Data validation error
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'VALIDATION_ERROR'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            # Generic server error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Dashboard API error: {str(e)}", exc_info=True)

            return Response(
                {
                    'error': {
                        'message': 'Internal server error',
                        'code': 'SERVER_ERROR'
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PerformanceViewSet(viewsets.ViewSet):
    """
    Performance Analysis API ViewSet.

    Provides endpoints for retrieving performance analysis data
    with optional filtering by date range, department, and project.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/performance/

        Retrieve performance analysis data with optional filters.

        Query Parameters:
        - startDate (optional): Start date (YYYY-MM-DD)
        - endDate (optional): End date (YYYY-MM-DD)
        - department (optional): Department filter
        - project (optional): Project filter

        Authentication: Required (JWT token via Bearer header)

        Response: 200 OK
        {
            "trendData": [
                {
                    "date": "2020-01-01",
                    "value": 75.5,
                    "target": 85.0
                },
                ...
            ],
            "departmentData": [
                {
                    "department": "컴퓨터공학과",
                    "value": 92.3,
                    "percentage": 15.2
                },
                ...
            ],
            "achievementData": {
                "actual": 83.5,
                "target": 85.0,
                "rate": 98.2,
                "status": "warning"
            }
        }

        Error Responses:
        - 400 Bad Request: Invalid filter parameters
        - 401 Unauthorized: Invalid/missing JWT token
        - 500 Internal Server Error: Server error
        """
        try:
            # 1. Validate filters
            filter_serializer = PerformanceFilterSerializer(
                data=request.query_params
            )
            filter_serializer.is_valid(raise_exception=True)

            # 2. Set default dates if not provided
            filters = filter_serializer.validated_data
            end_date = filters.get('end_date') or datetime.now().date()
            start_date = filters.get('start_date') or (
                end_date - timedelta(days=365)
            )

            # Clean up empty string filters
            department = filters.get('department')
            if department == '':
                department = None

            project = filters.get('project')
            if project == '':
                project = None

            # 3. Initialize dependencies (Dependency Injection)
            repository = PerformanceRepository()
            service = PerformanceService(repository)
            use_case = GetPerformanceDataUseCase(repository, service)

            # 4. Execute use case
            result = use_case.execute(
                start_date=start_date,
                end_date=end_date,
                department=department,
                project=project
            )

            # 5. Serialize response
            serializer = PerformanceResponseSerializer(data=result)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Validation error from use case or serializer
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'VALIDATION_ERROR'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            # Generic server error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Performance API error: {str(e)}", exc_info=True)

            return Response(
                {
                    'error': {
                        'message': 'Failed to fetch performance data',
                        'code': 'SERVER_ERROR'
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PapersAnalyticsViewSet(viewsets.ViewSet):
    """
    Papers Analytics API ViewSet.

    Provides endpoints for retrieving publication analysis data.
    Supports filtering by year, journal grade, and field.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='analytics')
    def get_analytics(self, request):
        """
        GET /api/papers/analytics/

        Retrieve papers analytics data with optional filters.

        Query Parameters:
            - year (optional): Filter by year (e.g., 2023)
            - journal (optional): Filter by journal grade (SCI, KCI, SCOPUS, 기타)
            - field (optional): Filter by department/field

        Authentication: Required (JWT token via Bearer header)

        Response: 200 OK
        {
            "yearly_data": [
                {"year": 2021, "count": 45},
                {"year": 2022, "count": 52}
            ],
            "journal_data": [
                {"journal_grade": "SCI", "count": 80},
                {"journal_grade": "KCI", "count": 45}
            ],
            "field_data": [
                {"department": "공학부", "count": 67},
                {"department": "의학부", "count": 52}
            ],
            "has_data": true
        }

        Error Responses:
        - 400 Bad Request: Invalid filter parameters
        - 401 Unauthorized: Invalid/missing JWT token
        - 500 Internal Server Error: Server error
        """
        try:
            # Get filter parameters
            year = request.query_params.get('year', None)
            journal_grade = request.query_params.get('journal', None)
            field = request.query_params.get('field', None)

            # Convert year to int if provided
            if year:
                try:
                    year = int(year)
                except ValueError:
                    return Response(
                        {
                            'error': {
                                'message': 'Year must be an integer',
                                'code': 'INVALID_PARAMETER'
                            }
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Initialize use case
            from ..application.use_cases import GetPapersAnalyticsUseCase
            use_case = GetPapersAnalyticsUseCase()

            # Execute use case
            analytics_data = use_case.execute(
                year=year,
                journal_grade=journal_grade,
                field=field
            )

            # Serialize response
            from .serializers import PapersAnalyticsSerializer
            serializer = PapersAnalyticsSerializer(analytics_data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'VALIDATION_ERROR'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Papers analytics API error: {str(e)}", exc_info=True)

            return Response(
                {
                    'error': {
                        'message': 'Failed to fetch papers analytics data',
                        'code': 'SERVER_ERROR'
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BudgetAnalysisViewSet(viewsets.ViewSet):
    """
    ViewSet for budget analysis endpoints.

    Provides three main endpoints:
    - allocation: Department budget distribution
    - execution: Budget execution status with rates
    - trends: Year-over-year budget trends
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from ..application.use_cases import BudgetAnalysisUseCase
        self.use_case = BudgetAnalysisUseCase()

    @action(detail=False, methods=['get'])
    def allocation(self, request):
        """
        GET /api/budget/allocation/

        Get department-wise budget allocation.

        Query Parameters:
        - department (optional): Filter by department
        - year (optional): Filter by year (default: current year)
        - category (optional): Filter by budget category

        Returns:
        - 200: List of budget allocation items
        - 400: Invalid filter parameters
        - 401: Unauthorized
        """
        from .serializers import BudgetFilterSerializer, BudgetAllocationSerializer

        try:
            # Validate query parameters
            filter_serializer = BudgetFilterSerializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)

            filters = filter_serializer.validated_data

            # Execute use case
            result = self.use_case.get_budget_allocation(
                department=filters.get('department'),
                year=filters.get('year'),
                category=filters.get('category')
            )

            # Serialize response
            serializer = BudgetAllocationSerializer(result, many=True)

            return Response({
                'data': serializer.data,
                'total': len(serializer.data)
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'VALIDATION_ERROR'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except NotFoundError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'NOT_FOUND'
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Budget allocation API error: {str(e)}", exc_info=True)

            return Response(
                {
                    'error': {
                        'message': 'Failed to fetch budget allocation data',
                        'code': 'SERVER_ERROR'
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def execution(self, request):
        """
        GET /api/budget/execution/

        Get budget execution status by department.

        Query Parameters:
        - department (optional): Filter by department
        - year (optional): Filter by year
        - start_date (optional): Start date for execution filter
        - end_date (optional): End date for execution filter

        Returns:
        - 200: Execution status with rates and warnings
        - 400: Invalid parameters
        """
        from .serializers import (
            BudgetFilterSerializer,
            ExecutionStatusSerializer,
            ExecutionSummarySerializer
        )

        try:
            filter_serializer = BudgetFilterSerializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)

            filters = filter_serializer.validated_data

            result = self.use_case.get_execution_status(
                department=filters.get('department'),
                year=filters.get('year'),
                start_date=filters.get('start_date'),
                end_date=filters.get('end_date')
            )

            data_serializer = ExecutionStatusSerializer(result['data'], many=True)
            summary_serializer = ExecutionSummarySerializer(result['summary'])

            return Response({
                'data': data_serializer.data,
                'summary': summary_serializer.data
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'VALIDATION_ERROR'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Budget execution API error: {str(e)}", exc_info=True)

            return Response(
                {
                    'error': {
                        'message': 'Failed to fetch budget execution data',
                        'code': 'SERVER_ERROR'
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """
        GET /api/budget/trends/

        Get year-over-year budget trends.

        Query Parameters:
        - department (optional): Filter by department
        - start_year (optional): Start year for trends
        - end_year (optional): End year for trends

        Returns:
        - 200: Yearly budget trends data
        """
        from .serializers import BudgetFilterSerializer, YearlyTrendsSerializer

        try:
            filter_serializer = BudgetFilterSerializer(data=request.query_params)
            filter_serializer.is_valid(raise_exception=True)

            filters = filter_serializer.validated_data

            result = self.use_case.get_yearly_trends(
                department=filters.get('department'),
                start_year=filters.get('start_year'),
                end_year=filters.get('end_year')
            )

            serializer = YearlyTrendsSerializer(result, many=True)

            return Response({
                'data': serializer.data,
                'yearRange': {
                    'min': result[0]['year'] if result else None,
                    'max': result[-1]['year'] if result else None
                }
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {
                    'error': {
                        'message': str(e),
                        'code': 'VALIDATION_ERROR'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Budget trends API error: {str(e)}", exc_info=True)

            return Response(
                {
                    'error': {
                        'message': 'Failed to fetch budget trends data',
                        'code': 'SERVER_ERROR'
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UploadViewSet(viewsets.ViewSet):
    """
    Upload API ViewSet.

    Provides endpoints for file upload and upload history.
    Admin-only access for uploading data files.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from ..application.use_cases import UploadFileUseCase, GetUploadHistoryUseCase

        self.upload_use_case = UploadFileUseCase()
        self.history_use_case = GetUploadHistoryUseCase()

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        POST /api/upload/upload/

        Upload Excel file for data import.
        """
        from .serializers import UploadFileSerializer, UploadResultSerializer

        # Check admin permission
        if not request.user.is_staff:
            return Response(
                {'error': {'message': 'Admin permission required', 'code': 'PERMISSION_DENIED'}},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UploadFileSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {'error': {'message': str(e), 'code': 'VALIDATION_ERROR'}},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = serializer.validated_data['file']

        try:
            result = self.upload_use_case.execute(user_id=request.user.id, uploaded_file=uploaded_file)
            result_serializer = UploadResultSerializer(result)
            return Response(result_serializer.data, status=status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': {'message': str(e), 'code': 'VALIDATION_ERROR'}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Upload error: {str(e)}", exc_info=True)
            return Response({'error': {'message': 'Failed to process file', 'code': 'SERVER_ERROR'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        """
        GET /api/upload/history/

        Get upload history with pagination.
        """
        from .serializers import UploadHistoryListSerializer

        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))

            result = self.history_use_case.execute(
                user_id=request.user.id,
                page=page,
                page_size=page_size,
                is_admin=request.user.is_staff
            )

            serializer = UploadHistoryListSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Upload history error: {str(e)}", exc_info=True)
            return Response({'error': {'message': 'Failed to fetch upload history', 'code': 'SERVER_ERROR'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
