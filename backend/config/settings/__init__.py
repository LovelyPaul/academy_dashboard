"""
Settings package initialization
"""
import os

# Default to development settings
DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
