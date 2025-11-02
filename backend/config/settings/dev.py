"""
Development settings
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Development-specific CORS settings
CORS_ALLOW_ALL_ORIGINS = True
