"""
Students Analytics Serializers.
Handles serialization of students analytics data for API responses.
Follows DRF best practices and common-modules.md specifications.
"""
from rest_framework import serializers


class DepartmentStatSerializer(serializers.Serializer):
    """Serializer for department statistics."""
    college = serializers.CharField()
    department = serializers.CharField()
    student_count = serializers.IntegerField()


class GradeDistributionSerializer(serializers.Serializer):
    """Serializer for grade distribution."""
    program_type = serializers.CharField()
    grade = serializers.IntegerField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()


class EnrollmentTrendSerializer(serializers.Serializer):
    """Serializer for enrollment trend."""
    year = serializers.IntegerField()
    admission_count = serializers.IntegerField()
    graduation_count = serializers.IntegerField()


class StudentsAnalyticsSerializer(serializers.Serializer):
    """Main serializer for students analytics response."""
    department_stats = DepartmentStatSerializer(many=True)
    grade_distribution = GradeDistributionSerializer(many=True)
    enrollment_trend = EnrollmentTrendSerializer(many=True)
