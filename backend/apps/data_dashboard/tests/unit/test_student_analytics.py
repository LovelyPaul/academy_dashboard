"""
Unit tests for Student Analytics module.
Tests repository, service, and use case layers.
"""
from django.test import TestCase
from apps.data_dashboard.models import Student
from apps.data_dashboard.infrastructure.repositories import StudentRepository
from apps.data_dashboard.domain.services import StudentAnalyticsService
from apps.data_dashboard.application.use_cases import GetStudentsAnalyticsUseCase
from core.exceptions import ValidationError


class TestStudentRepository(TestCase):
    """Test StudentRepository methods."""

    def setUp(self):
        """Create test data."""
        Student.objects.create(
            student_id='2020001',
            name='홍길동',
            college='공과대학',
            department='컴퓨터공학과',
            grade=4,
            program_type='학사',
            enrollment_status='재학',
            admission_year=2020
        )
        Student.objects.create(
            student_id='2021001',
            name='김영희',
            college='공과대학',
            department='전자공학과',
            grade=3,
            program_type='학사',
            enrollment_status='재학',
            admission_year=2021
        )

    def test_get_department_stats_no_filter(self):
        """Test department stats without filters."""
        result = StudentRepository.get_department_stats({})
        self.assertEqual(result.count(), 2)

    def test_get_department_stats_with_department_filter(self):
        """Test department stats with department filter."""
        result = StudentRepository.get_department_stats({'department': '컴퓨터공학과'})
        self.assertEqual(result.count(), 1)
        self.assertEqual(result[0]['student_count'], 1)

    def test_get_grade_distribution(self):
        """Test grade distribution."""
        result = StudentRepository.get_grade_distribution({})
        self.assertGreater(result.count(), 0)

    def test_get_enrollment_trend(self):
        """Test enrollment trend."""
        result = StudentRepository.get_enrollment_trend({})
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


class TestStudentAnalyticsService(TestCase):
    """Test StudentAnalyticsService methods."""

    def test_calculate_statistics_with_data(self):
        """Test statistics calculation with valid data."""
        dept_stats = [
            {'department': '컴퓨터공학과', 'student_count': 100},
            {'department': '전자공학과', 'student_count': 80}
        ]
        result = StudentAnalyticsService.calculate_statistics(dept_stats)

        self.assertEqual(result['total_students'], 180)
        self.assertEqual(result['department_count'], 2)
        self.assertEqual(result['average_per_department'], 90.0)
        self.assertEqual(result['largest_department'], '컴퓨터공학과')

    def test_calculate_statistics_empty_data(self):
        """Test statistics calculation with empty data."""
        result = StudentAnalyticsService.calculate_statistics([])
        self.assertEqual(result['total_students'], 0)

    def test_format_grade_distribution(self):
        """Test grade distribution formatting."""
        grade_data = [
            {'program_type': '학사', 'grade': 1, 'count': 50},
            {'program_type': '학사', 'grade': 2, 'count': 50}
        ]
        result = StudentAnalyticsService.format_grade_distribution(grade_data)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['percentage'], 50.0)

    def test_validate_filters_valid(self):
        """Test filter validation with valid filters."""
        filters = {'department': '컴퓨터공학과', 'grade': 1, 'year': 2023}
        result = StudentAnalyticsService.validate_filters(filters)

        self.assertEqual(result['department'], '컴퓨터공학과')
        self.assertEqual(result['grade'], 1)
        self.assertEqual(result['year'], 2023)

    def test_validate_filters_invalid_grade(self):
        """Test filter validation with invalid grade."""
        filters = {'grade': 10}
        with self.assertRaises(ValidationError):
            StudentAnalyticsService.validate_filters(filters)


class TestGetStudentsAnalyticsUseCase(TestCase):
    """Test GetStudentsAnalyticsUseCase."""

    def setUp(self):
        """Create test data."""
        Student.objects.create(
            student_id='2020001',
            name='Test Student',
            college='공과대학',
            department='컴퓨터공학과',
            grade=1,
            program_type='학사',
            enrollment_status='재학',
            admission_year=2020
        )

    def test_execute_success(self):
        """Test successful execution."""
        use_case = GetStudentsAnalyticsUseCase()
        result = use_case.execute({})

        self.assertIn('department_stats', result)
        self.assertIn('grade_distribution', result)
        self.assertIn('enrollment_trend', result)

    def test_execute_with_filters(self):
        """Test execution with filters."""
        use_case = GetStudentsAnalyticsUseCase()
        result = use_case.execute({'department': '컴퓨터공학과'})

        self.assertIsInstance(result, dict)

    def test_execute_invalid_filters(self):
        """Test execution with invalid filters."""
        use_case = GetStudentsAnalyticsUseCase()
        with self.assertRaises(ValidationError):
            use_case.execute({'grade': 'invalid'})
