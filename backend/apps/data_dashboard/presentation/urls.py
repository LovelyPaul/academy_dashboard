"""
URL configuration for data dashboard app.
Following the common-modules.md specification.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DashboardViewSet, PerformanceViewSet, PapersAnalyticsViewSet, BudgetAnalysisViewSet, UploadViewSet
from .views.students_views import StudentsViewSet

app_name = 'data_dashboard'

# Router for ViewSets
router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'performance', PerformanceViewSet, basename='performance')
router.register(r'papers', PapersAnalyticsViewSet, basename='papers')
router.register(r'students', StudentsViewSet, basename='students')
router.register(r'budget', BudgetAnalysisViewSet, basename='budget')
router.register(r'upload', UploadViewSet, basename='upload')

urlpatterns = [
    # Dashboard API endpoints
    path('', include(router.urls)),
]
