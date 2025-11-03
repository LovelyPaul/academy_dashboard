"""
User use cases for orchestrating business flows.
Following the common-modules.md specification.
Implements application layer logic for user operations.
"""
import logging
from ..domain.services import UserService
from ..infrastructure.repositories import UserRepository

logger = logging.getLogger(__name__)


class UserWebhookUseCase:
    """
    Use case for handling Clerk webhook events.
    Orchestrates the flow of user synchronization from Clerk.
    Follows SRP by handling only webhook event processing.
    """

    def __init__(self, user_service: UserService = None, user_repository: UserRepository = None):
        """
        Initialize UserWebhookUseCase with dependency injection.

        Args:
            user_service: UserService instance (DIP compliance)
            user_repository: UserRepository instance (DIP compliance)
        """
        self.user_repository = user_repository or UserRepository()
        self.user_service = user_service or UserService(self.user_repository)

    def handle_event(self, event_type: str, event_data: dict):
        """
        Handle Clerk webhook event.
        Orchestrates the appropriate service method based on event type.

        Args:
            event_type: Type of Clerk event (e.g., 'user.created', 'user.updated', 'user.deleted')
            event_data: Event data from Clerk webhook

        Raises:
            ValueError: If required event data is missing
        """
        # Extract user data from event
        clerk_id = event_data.get('id')
        email_addresses = event_data.get('email_addresses', [])

        # Try to get email from email_addresses array or primary_email_address_id
        email = None
        if email_addresses and len(email_addresses) > 0:
            # Handle both dict format and potential nested structure
            if isinstance(email_addresses[0], dict):
                email = email_addresses[0].get('email_address')
            elif isinstance(email_addresses[0], str):
                email = email_addresses[0]

        # Fallback to other possible email fields
        if not email:
            email = event_data.get('email') or event_data.get('primary_email_address')

        first_name = event_data.get('first_name')
        last_name = event_data.get('last_name')

        # Log event data for debugging
        logger.info(f"Processing {event_type} event - clerk_id: {clerk_id}, email: {email}")

        # Validate required fields
        if not clerk_id or not email:
            error_msg = f"Invalid Clerk webhook event data: missing clerk_id or email for type {event_type}. Event data: {event_data.keys()}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Route to appropriate handler
        if event_type == 'user.created':
            self._handle_user_created(clerk_id, email, first_name, last_name)
        elif event_type == 'user.updated':
            self._handle_user_updated(clerk_id, email, first_name, last_name)
        elif event_type == 'user.deleted':
            self._handle_user_deleted(clerk_id)
        else:
            logger.warning(f"Unhandled Clerk webhook event type: {event_type}")

    def _handle_user_created(self, clerk_id: str, email: str,
                             first_name: str = None, last_name: str = None):
        """
        Handle user.created event.

        Args:
            clerk_id: Clerk user ID
            email: User email
            first_name: User first name
            last_name: User last name
        """
        try:
            user = self.user_service.create_user_from_clerk(
                clerk_id=clerk_id,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            logger.info(f"Successfully handled user.created event for {email}")
        except Exception as e:
            logger.error(f"Error handling user.created event for {email}: {e}", exc_info=True)
            raise

    def _handle_user_updated(self, clerk_id: str, email: str,
                             first_name: str = None, last_name: str = None):
        """
        Handle user.updated event.

        Args:
            clerk_id: Clerk user ID
            email: User email
            first_name: User first name
            last_name: User last name
        """
        try:
            user = self.user_service.update_user_from_clerk(
                clerk_id=clerk_id,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            logger.info(f"Successfully handled user.updated event for {email}")
        except Exception as e:
            logger.error(f"Error handling user.updated event for {email}: {e}", exc_info=True)
            raise

    def _handle_user_deleted(self, clerk_id: str):
        """
        Handle user.deleted event.

        Args:
            clerk_id: Clerk user ID
        """
        try:
            self.user_service.delete_user_from_clerk(clerk_id=clerk_id)
            logger.info(f"Successfully handled user.deleted event for clerk_id {clerk_id}")
        except Exception as e:
            logger.error(f"Error handling user.deleted event for clerk_id {clerk_id}: {e}", exc_info=True)
            raise
