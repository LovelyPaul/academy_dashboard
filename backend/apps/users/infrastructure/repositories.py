"""
User repository for database operations.
Following the common-modules.md specification.
Implements Repository pattern for User model.
"""
import logging
from django.db import IntegrityError
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


class UserRepository:
    """
    User repository for CRUD operations.
    Follows DIP (Dependency Inversion Principle) by providing
    an abstraction layer between domain logic and data persistence.
    """

    def get_by_clerk_id(self, clerk_id: str):
        """
        Get user by Clerk ID.

        Args:
            clerk_id: Clerk user ID

        Returns:
            User object or None
        """
        try:
            return User.objects.get(clerk_id=clerk_id)
        except User.DoesNotExist:
            return None

    def get_by_email(self, email: str):
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User object or None
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def create_user(self, clerk_id: str, email: str, first_name: str = None,
                    last_name: str = None, username: str = None, role: str = 'user'):
        """
        Create new user.

        Args:
            clerk_id: Clerk user ID
            email: User email
            first_name: User first name
            last_name: User last name
            username: Username (defaults to email if not provided)
            role: User role (default: 'user')

        Returns:
            Created User object

        Raises:
            ValueError: If user creation fails due to data integrity issue
        """
        try:
            if not username:
                username = email

            user = User.objects.create(
                clerk_id=clerk_id,
                email=email,
                username=username,
                first_name=first_name or '',
                last_name=last_name or '',
                role=role
            )
            logger.info(f"User created: {email} (Clerk ID: {clerk_id})")
            return user

        except IntegrityError as e:
            logger.error(f"Integrity error creating user {email}: {e}")
            raise ValueError(f"User creation failed due to data integrity issue: {e}")

    def update_user(self, user, email: str = None, first_name: str = None,
                    last_name: str = None, role: str = None):
        """
        Update existing user.

        Args:
            user: User object to update
            email: New email (optional)
            first_name: New first name (optional)
            last_name: New last name (optional)
            role: New role (optional)

        Returns:
            Updated User object
        """
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if role is not None:
            user.role = role

        user.save()
        logger.info(f"User updated: {user.email} (Clerk ID: {user.clerk_id})")
        return user

    def delete_user(self, user):
        """
        Delete user.

        Args:
            user: User object to delete
        """
        email = user.email
        clerk_id = user.clerk_id
        user.delete()
        logger.info(f"User deleted: {email} (Clerk ID: {clerk_id})")

    def list_all_users(self):
        """
        List all users.

        Returns:
            QuerySet of all users
        """
        return User.objects.all()

    def list_admin_users(self):
        """
        List all admin users.

        Returns:
            QuerySet of admin users
        """
        return User.objects.filter(role='admin')
