"""
Clerk authentication middleware for JWT token verification.
Following the common-modules.md specification.
"""
import logging
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

logger = logging.getLogger(__name__)


class ClerkAuthenticationMiddleware:
    """
    Clerk JWT token verification middleware.
    Verifies the JWT token from Authorization header and injects user into request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract Authorization header
        auth_header = request.headers.get('Authorization', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Verify Clerk JWT token
                user = self._verify_clerk_token(token)
                request.user = user
                logger.info(f"User authenticated: {user}, is_authenticated: {user.is_authenticated if hasattr(user, 'is_authenticated') else 'N/A'}")
            except Exception as e:
                logger.warning(f"Clerk token verification failed: {e}")
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response

    def _verify_clerk_token(self, token):
        """
        Verify Clerk JWT token and return user.

        Note: This is a simplified implementation. In production, use
        the Clerk SDK to properly verify the JWT signature and claims.
        """
        from apps.users.models import User

        # TODO: Implement proper Clerk JWT verification using clerk-sdk-python
        # For now, this is a placeholder that assumes the token is valid
        # In production, decode and verify the JWT using Clerk's public key

        try:
            import jwt
            from jwt import PyJWKClient

            # Decode token without verification for now (development only)
            # In production, fetch Clerk JWKS and verify signature
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            clerk_id = decoded_token.get('sub')

            if clerk_id:
                # Try to get existing user, or create new one (temporary solution)
                try:
                    user = User.objects.get(clerk_id=clerk_id)
                except User.DoesNotExist:
                    # Auto-create user from JWT token (temporary for development)
                    email = decoded_token.get('email', f'{clerk_id}@temp.com')
                    username = email.split('@')[0] if email else clerk_id[:30]

                    user = User.objects.create(
                        clerk_id=clerk_id,
                        email=email,
                        username=username[:150],  # Django username max length
                        first_name=decoded_token.get('given_name', ''),
                        last_name=decoded_token.get('family_name', ''),
                    )
                    logger.info(f"Auto-created user from JWT token: {email}")

                return user
            else:
                return AnonymousUser()

        except jwt.DecodeError as e:
            logger.warning(f"Token decode error: {e}")
            return AnonymousUser()
        except Exception as e:
            logger.error(f"Unexpected error in token verification: {e}")
            return AnonymousUser()
