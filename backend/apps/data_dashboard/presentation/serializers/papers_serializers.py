"""
Papers Analytics Serializers

Serializers for papers analytics API responses.
"""

from rest_framework import serializers


class YearlyDataSerializer(serializers.Serializer):
    """Serializer for yearly publication data."""
    year = serializers.IntegerField()
    count = serializers.IntegerField()


class JournalDataSerializer(serializers.Serializer):
    """Serializer for journal distribution data."""
    journal_grade = serializers.CharField(max_length=50)
    count = serializers.IntegerField()


class FieldDataSerializer(serializers.Serializer):
    """Serializer for field statistics data."""
    department = serializers.CharField(max_length=100)
    count = serializers.IntegerField()


class PapersAnalyticsSerializer(serializers.Serializer):
    """Serializer for complete papers analytics response."""
    yearly_data = YearlyDataSerializer(many=True)
    journal_data = JournalDataSerializer(many=True)
    field_data = FieldDataSerializer(many=True)
    has_data = serializers.BooleanField()
