"""
Unit tests for PapersAnalyticsService
Tests business logic for papers analytics data aggregation.
"""
import pytest
from unittest.mock import Mock, MagicMock
from apps.data_dashboard.domain.services import PapersAnalyticsService
from apps.data_dashboard.infrastructure.repositories import PapersAnalyticsRepository


class TestPapersAnalyticsService:
    """Unit tests for PapersAnalyticsService."""

    @pytest.fixture
    def mock_repository(self):
        """Create mock repository."""
        return Mock(spec=PapersAnalyticsRepository)

    @pytest.fixture
    def service(self, mock_repository):
        """Create service instance with mock repository."""
        return PapersAnalyticsService(mock_repository)

    def test_get_analytics_no_filters(self, service, mock_repository):
        """Test get_analytics without filters."""
        # Arrange
        mock_repository.get_yearly_data.return_value = [
            {"year": 2021, "count": 45},
            {"year": 2022, "count": 52}
        ]
        mock_repository.get_journal_distribution.return_value = [
            {"journal_grade": "SCI", "count": 80}
        ]
        mock_repository.get_field_statistics.return_value = [
            {"department": "공학부", "count": 67}
        ]

        # Act
        result = service.get_analytics()

        # Assert
        assert len(result['yearly_data']) == 2
        assert len(result['journal_data']) == 1
        assert len(result['field_data']) == 1
        mock_repository.get_yearly_data.assert_called_once_with(None, None, None)

    def test_get_analytics_with_year_filter(self, service, mock_repository):
        """Test get_analytics with year filter."""
        # Arrange
        mock_repository.get_yearly_data.return_value = [
            {"year": 2023, "count": 61}
        ]
        mock_repository.get_journal_distribution.return_value = []
        mock_repository.get_field_statistics.return_value = []

        # Act
        result = service.get_analytics(year=2023)

        # Assert
        assert len(result['yearly_data']) == 1
        assert result['yearly_data'][0]['year'] == 2023
        mock_repository.get_yearly_data.assert_called_once_with(2023, None, None)

    def test_get_analytics_with_multiple_filters(self, service, mock_repository):
        """Test get_analytics with multiple filters."""
        # Arrange
        mock_repository.get_yearly_data.return_value = [
            {"year": 2023, "count": 30}
        ]
        mock_repository.get_journal_distribution.return_value = [
            {"journal_grade": "SCI", "count": 30}
        ]
        mock_repository.get_field_statistics.return_value = [
            {"department": "공학부", "count": 30}
        ]

        # Act
        result = service.get_analytics(year=2023, journal_grade="SCI", field="공학")

        # Assert
        assert len(result['yearly_data']) == 1
        assert len(result['journal_data']) == 1
        assert len(result['field_data']) == 1
        mock_repository.get_yearly_data.assert_called_once_with(2023, "SCI", "공학")

    def test_validate_filters_valid(self, service):
        """Test validate_filters with valid parameters."""
        assert service.validate_filters(2023, "SCI", "공학") is True

    def test_validate_filters_valid_with_none(self, service):
        """Test validate_filters with None values."""
        assert service.validate_filters(None, None, None) is True

    def test_validate_filters_invalid_year_too_low(self, service):
        """Test validate_filters with invalid year (too low)."""
        assert service.validate_filters(1999, None, None) is False

    def test_validate_filters_invalid_year_too_high(self, service):
        """Test validate_filters with invalid year (too high)."""
        assert service.validate_filters(2101, None, None) is False

    def test_validate_filters_invalid_journal(self, service):
        """Test validate_filters with invalid journal grade."""
        assert service.validate_filters(None, "INVALID", None) is False

    def test_validate_filters_valid_journal_grades(self, service):
        """Test validate_filters with all valid journal grades."""
        assert service.validate_filters(None, "SCI", None) is True
        assert service.validate_filters(None, "KCI", None) is True
        assert service.validate_filters(None, "SCOPUS", None) is True
        assert service.validate_filters(None, "기타", None) is True

    def test_get_analytics_empty_data(self, service, mock_repository):
        """Test get_analytics when repository returns empty data."""
        # Arrange
        mock_repository.get_yearly_data.return_value = []
        mock_repository.get_journal_distribution.return_value = []
        mock_repository.get_field_statistics.return_value = []

        # Act
        result = service.get_analytics()

        # Assert
        assert len(result['yearly_data']) == 0
        assert len(result['journal_data']) == 0
        assert len(result['field_data']) == 0

    def test_get_analytics_with_journal_filter(self, service, mock_repository):
        """Test get_analytics with journal grade filter."""
        # Arrange
        mock_repository.get_yearly_data.return_value = [
            {"year": 2023, "count": 40}
        ]
        mock_repository.get_journal_distribution.return_value = [
            {"journal_grade": "KCI", "count": 40}
        ]
        mock_repository.get_field_statistics.return_value = [
            {"department": "의학부", "count": 40}
        ]

        # Act
        result = service.get_analytics(journal_grade="KCI")

        # Assert
        mock_repository.get_yearly_data.assert_called_once_with(None, "KCI", None)
        assert len(result['journal_data']) == 1

    def test_get_analytics_with_field_filter(self, service, mock_repository):
        """Test get_analytics with field filter."""
        # Arrange
        mock_repository.get_yearly_data.return_value = [
            {"year": 2023, "count": 25}
        ]
        mock_repository.get_journal_distribution.return_value = []
        mock_repository.get_field_statistics.return_value = [
            {"department": "자연과학부", "count": 25}
        ]

        # Act
        result = service.get_analytics(field="자연과학")

        # Assert
        mock_repository.get_yearly_data.assert_called_once_with(None, None, "자연과학")
        assert len(result['field_data']) == 1
