"""
User model for Clerk synchronization.
Following the common-modules.md and database.md specifications.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for Clerk synchronization.
    Extends Django's AbstractUser with Clerk-specific fields.
    """
    clerk_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Clerk User ID"
    )
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('user', 'User')],
        default='user',
        help_text="User role"
    )

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['clerk_id']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'
