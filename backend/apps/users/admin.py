"""
Django admin configuration for users app.
"""
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'clerk_id', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'clerk_id', 'first_name', 'last_name')
    readonly_fields = ('clerk_id', 'date_joined', 'last_login')
