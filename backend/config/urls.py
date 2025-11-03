"""
URL configuration for university dashboard project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint for Railway"""
    return JsonResponse({"status": "healthy"})

def debug_env(request):
    """Debug endpoint to check environment variables"""
    import os
    from django.conf import settings
    return JsonResponse({
        "DATABASE_URL_exists": bool(os.getenv('DATABASE_URL')),
        "DATABASE_URL_length": len(os.getenv('DATABASE_URL', '')),
        "DATABASE_URL_starts_with": os.getenv('DATABASE_URL', '')[:20] if os.getenv('DATABASE_URL') else None,
        "DATABASES_HOST": settings.DATABASES['default'].get('HOST', 'NOT SET'),
        "CLERK_WEBHOOK_SECRET_exists": bool(os.getenv('CLERK_WEBHOOK_SECRET')),
        "DJANGO_SETTINGS_MODULE": os.getenv('DJANGO_SETTINGS_MODULE'),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('api/debug-env/', debug_env, name='debug_env'),
    path('api/users/', include('apps.users.presentation.urls')),
    path('api/dashboard/', include('apps.data_dashboard.presentation.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
