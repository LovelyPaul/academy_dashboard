"""
Students Analytics ViewSet.
REST API endpoints for student analytics data.
Follows DRF ViewSet pattern and SOLID principles.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.exceptions import ValidationError


class StudentsViewSet(viewsets.ViewSet):
    """ViewSet for student analytics endpoints."""

    permission_classes = [AllowAny]  # TODO: Change back to IsAuthenticated after webhook setup

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
            from ...models import Student
            from django.db.models import Count, Q

            # Extract filters from query params
            department_filter = request.query_params.get('department')
            grade_filter = request.query_params.get('grade')
            year_filter = request.query_params.get('year')

            # Build query
            query = Student.objects.filter(enrollment_status='재학')

            if department_filter:
                query = query.filter(department=department_filter)
            if grade_filter:
                query = query.filter(grade=int(grade_filter))
            if year_filter:
                query = query.filter(admission_year=int(year_filter))

            # Total students
            total_students = query.count()

            # Department stats (count by department)
            department_stats = list(
                Student.objects.filter(enrollment_status='재학')
                .values('department')
                .annotate(count=Count('id'))
                .order_by('-count')
            )

            # Grade distribution
            grade_distribution = list(
                Student.objects.filter(enrollment_status='재학')
                .values('grade')
                .annotate(count=Count('id'))
                .order_by('grade')
            )

            # Enrollment trend (by admission year)
            enrollment_trend = list(
                Student.objects.values('admission_year')
                .annotate(
                    total=Count('id'),
                    enrolled=Count('id', filter=Q(enrollment_status='재학'))
                )
                .order_by('admission_year')
            )

            data = {
                'total_students': total_students,
                'department_stats': department_stats,
                'grade_distribution': grade_distribution,
                'enrollment_trend': enrollment_trend
            }

            return Response(data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(
                {'error': 'validation_error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': 'server_error', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
