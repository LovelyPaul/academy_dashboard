"""
URL configuration for users app.
Following the common-modules.md specification.
"""
from django.urls import path
from ..infrastructure.clerk_webhook_views import clerk_webhook_handler

app_name = 'users'

urlpatterns = [
    path('webhooks/clerk/', clerk_webhook_handler, name='clerk_webhook'),
]
