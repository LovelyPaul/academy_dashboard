"""
Papers Analytics Views

API endpoints for papers analytics.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.exceptions import ValidationError, AuthenticationError
from apps.data_dashboard.application.use_cases.get_papers_analytics import GetPapersAnalyticsUseCase
from apps.data_dashboard.presentation.serializers.papers_serializers import PapersAnalyticsSerializer


class PapersAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet for papers analytics endpoints."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_case = GetPapersAnalyticsUseCase()

    @action(detail=False, methods=['get'], url_path='analytics')
    def get_analytics(self, request):
        """
        Get papers analytics data.

        Query Parameters:
            - year (optional): Filter by year
            - journal (optional): Filter by journal grade
            - field (optional): Filter by department/field

        Response:
            200 OK: Analytics data
            400 Bad Request: Invalid filters
            401 Unauthorized: Not authenticated
        """
        # Check authentication (temporarily disabled for development)
        # TODO: Re-enable after webhook setup
        # if not request.user or not request.user.is_authenticated:
        #     raise AuthenticationError("Authentication required")

        # Get filter parameters
        year = request.query_params.get('year', None)
        journal_grade = request.query_params.get('journal', None)
        field = request.query_params.get('field', None)

        # Convert year to int if provided
        if year:
            try:
                year = int(year)
            except ValueError:
                raise ValidationError("Year must be an integer")

        try:
            # Execute use case
            analytics_data = self.use_case.execute(
                year=year,
                journal_grade=journal_grade,
                field=field
            )

            # Serialize response
            serializer = PapersAnalyticsSerializer(analytics_data)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
