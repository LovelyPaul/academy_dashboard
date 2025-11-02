"""
Data dashboard app configuration.
"""
from django.apps import AppConfig


class DataDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.data_dashboard'
    label = 'data_dashboard'
