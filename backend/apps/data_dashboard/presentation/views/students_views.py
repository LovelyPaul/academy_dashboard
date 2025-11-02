"""
Students Analytics ViewSet.
REST API endpoints for student analytics data.
Follows DRF ViewSet pattern and SOLID principles.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.exceptions import ValidationError
from apps.data_dashboard.application.use_cases.get_students_analytics_use_case import GetStudentsAnalyticsUseCase
from apps.data_dashboard.presentation.serializers.students_serializers import StudentsAnalyticsSerializer


class StudentsViewSet(viewsets.ViewSet):
    """ViewSet for student analytics endpoints."""

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        """
        Get student analytics data.

        Query Parameters:
            - department (optional): Department name filter
            - grade (optional): Grade filter (0-4)
            - year (optional): Admission year filter

        Returns:
            200: Analytics data
            400: Invalid filters
            401: Unauthorized
            500: Server error
        """
        try:
            # Extract filters from query params
            filters = {
                'department': request.query_params.get('department'),
                'grade': request.query_params.get('grade'),
                'year': request.query_params.get('year'),
            }

            # Execute use case
            use_case = GetStudentsAnalyticsUseCase()
            data = use_case.execute(filters)

            # Serialize response
            serializer = StudentsAnalyticsSerializer(data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {'error': 'validation_error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'server_error', 'message': 'An error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
