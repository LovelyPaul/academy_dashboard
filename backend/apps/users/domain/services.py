"""
User domain service containing business logic.
Following the common-modules.md specification.
Implements pure business logic separated from persistence layer.
"""
import logging
from django.db import transaction
from ..infrastructure.repositories import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    """
    User service for business logic.
    Follows SRP (Single Responsibility Principle) by handling
    only user-related business rules and logic.
    """

    def __init__(self, user_repository: UserRepository = None):
        """
        Initialize UserService with dependency injection.

        Args:
            user_repository: UserRepository instance (DIP compliance)
        """
        self.user_repository = user_repository or UserRepository()

    @transaction.atomic
    def create_user_from_clerk(self, clerk_id: str, email: str,
                                first_name: str = None, last_name: str = None):
        """
        Create user from Clerk webhook data.
        Business logic: Check if user exists, create if not.

        Args:
            clerk_id: Clerk user ID
            email: User email
            first_name: User first name
            last_name: User last name

        Returns:
            User object
        """
        # Check if user already exists
        existing_user = self.user_repository.get_by_clerk_id(clerk_id)
        if existing_user:
            logger.info(f"User with clerk_id {clerk_id} already exists, skipping creation.")
            return existing_user

        # Create new user
        user = self.user_repository.create_user(
            clerk_id=clerk_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=email,
            role='user'
        )

        # Business logic: Perform post-creation tasks
        self._on_user_created(user)

        return user

    @transaction.atomic
    def update_user_from_clerk(self, clerk_id: str, email: str,
                                first_name: str = None, last_name: str = None):
        """
        Update user from Clerk webhook data.
        Business logic: If user doesn't exist, create it.

        Args:
            clerk_id: Clerk user ID
            email: User email
            first_name: User first name
            last_name: User last name

        Returns:
            User object
        """
        user = self.user_repository.get_by_clerk_id(clerk_id)

        if user:
            # Update existing user
            user = self.user_repository.update_user(
                user=user,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            logger.info(f"User {email} (Clerk ID: {clerk_id}) updated successfully.")
        else:
            # User doesn't exist, create it
            logger.warning(f"User with clerk_id {clerk_id} not found for update. Creating new user.")
            user = self.create_user_from_clerk(clerk_id, email, first_name, last_name)

        return user

    @transaction.atomic
    def delete_user_from_clerk(self, clerk_id: str):
        """
        Delete user from Clerk webhook data.

        Args:
            clerk_id: Clerk user ID
        """
        user = self.user_repository.get_by_clerk_id(clerk_id)

        if user:
            # Business logic: Perform pre-deletion tasks
            self._on_user_deleted(user)

            # Delete user
            self.user_repository.delete_user(user)
            logger.info(f"User with clerk_id {clerk_id} deleted successfully.")
        else:
            logger.warning(f"User with clerk_id {clerk_id} not found for deletion.")

    def _on_user_created(self, user):
        """
        Business logic to execute after user creation.
        E.g., Send welcome email, create default dashboard settings, etc.

        Args:
            user: Created User object
        """
        logger.info(f"Executing post-creation logic for user {user.email}")
        # TODO: Add business logic here (e.g., create default user preferences)
        pass

    def _on_user_deleted(self, user):
        """
        Business logic to execute before user deletion.
        E.g., Clean up user data, send notification, etc.

        Args:
            user: User object to be deleted
        """
        logger.info(f"Executing pre-deletion logic for user {user.email}")
        # TODO: Add business logic here (e.g., archive user data)
        pass

    def promote_to_admin(self, clerk_id: str):
        """
        Promote user to admin role.
        Business logic for role management.

        Args:
            clerk_id: Clerk user ID

        Returns:
            Updated User object

        Raises:
            ValueError: If user not found
        """
        user = self.user_repository.get_by_clerk_id(clerk_id)
        if not user:
            raise ValueError(f"User with clerk_id {clerk_id} not found")

        user = self.user_repository.update_user(user=user, role='admin')
        logger.info(f"User {user.email} promoted to admin")
        return user

    def demote_from_admin(self, clerk_id: str):
        """
        Demote user from admin role.
        Business logic for role management.

        Args:
            clerk_id: Clerk user ID

        Returns:
            Updated User object

        Raises:
            ValueError: If user not found
        """
        user = self.user_repository.get_by_clerk_id(clerk_id)
        if not user:
            raise ValueError(f"User with clerk_id {clerk_id} not found")

        user = self.user_repository.update_user(user=user, role='user')
        logger.info(f"User {user.email} demoted from admin")
        return user
