"""
Standard pagination class for API responses.
Following the common-modules.md specification.
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class.
    - Default page size: 20 items
    - Maximum page size: 100 items
    - Page size can be customized via page_size query parameter
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
