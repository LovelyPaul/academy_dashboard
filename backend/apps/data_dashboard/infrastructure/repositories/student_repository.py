"""
StudentRepository: Data access layer for Student model.
Provides methods for querying student data with various filters.
Follows the Infrastructure layer pattern from architecture.md.
"""
from django.db.models import QuerySet, Count
from typing import Dict, List
from apps.data_dashboard.models import Student


class StudentRepository:
    """Repository for Student model database operations."""

    @staticmethod
    def get_department_stats(filters: Dict) -> QuerySet:
        """
        Get student count by department.

        Args:
            filters: Dictionary containing optional filters
                - department: str
                - grade: int
                - year: int (admission_year)
                - enrollment_status: str (default: '재학')

        Returns:
            QuerySet with annotations: college, department, student_count
        """
        queryset = Student.objects.filter(enrollment_status='재학')

        if filters.get('department'):
            queryset = queryset.filter(department=filters['department'])
        if filters.get('grade') is not None:
            queryset = queryset.filter(grade=filters['grade'])
        if filters.get('year'):
            queryset = queryset.filter(admission_year=filters['year'])

        return queryset.values('college', 'department').annotate(
            student_count=Count('id')
        ).order_by('-student_count')

    @staticmethod
    def get_grade_distribution(filters: Dict) -> QuerySet:
        """
        Get student count by program type and grade.

        Args:
            filters: Same as get_department_stats

        Returns:
            QuerySet with annotations: program_type, grade, count
        """
        queryset = Student.objects.filter(enrollment_status='재학')

        if filters.get('department'):
            queryset = queryset.filter(department=filters['department'])
        if filters.get('year'):
            queryset = queryset.filter(admission_year=filters['year'])

        return queryset.values('program_type', 'grade').annotate(
            count=Count('id')
        ).order_by('program_type', 'grade')

    @staticmethod
    def get_enrollment_trend(filters: Dict) -> List[Dict]:
        """
        Get admission and graduation trends by year.

        Args:
            filters: Optional department filter

        Returns:
            List of dictionaries with year, admission_count, graduation_count
        """
        queryset = Student.objects.all()

        if filters.get('department'):
            queryset = queryset.filter(department=filters['department'])

        # Admission counts
        admissions = queryset.values('admission_year').annotate(
            count=Count('id')
        ).order_by('admission_year')

        # Graduation counts (approximation: students with status '졸업')
        graduations = queryset.filter(
            enrollment_status='졸업'
        ).values('admission_year').annotate(
            count=Count('id')
        ).order_by('admission_year')

        # Merge data
        years = {}
        for item in admissions:
            years[item['admission_year']] = {
                'year': item['admission_year'],
                'admission_count': item['count'],
                'graduation_count': 0
            }

        for item in graduations:
            year = item['admission_year']
            if year in years:
                years[year]['graduation_count'] = item['count']

        return list(years.values())
