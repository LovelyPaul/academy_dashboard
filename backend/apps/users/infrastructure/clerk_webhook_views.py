"""
Clerk webhook handler view.
Following the common-modules.md and clerk.md specifications.
Implements presentation layer for Clerk webhook integration.
"""
import json
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from svix.webhooks import Webhook, WebhookVerificationError

from ..application.use_cases import UserWebhookUseCase

logger = logging.getLogger(__name__)


@csrf_exempt
def clerk_webhook_handler(request):
    """
    Handle Clerk webhook requests.
    Verifies webhook signature and processes user events.

    This endpoint receives events from Clerk when user-related
    actions occur (user.created, user.updated, user.deleted).

    Args:
        request: HTTP request from Clerk

    Returns:
        JSON response with status
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST requests are allowed.")

    # Get webhook secret from settings
    webhook_secret = settings.CLERK_WEBHOOK_SECRET
    if not webhook_secret:
        logger.error("CLERK_WEBHOOK_SECRET is not set in settings.")
        return HttpResponseBadRequest("Webhook secret not configured.")

    # Extract Svix headers for verification
    headers = request.headers
    payload = request.body.decode('utf-8')

    svix_id = headers.get('svix-id')
    svix_timestamp = headers.get('svix-timestamp')
    svix_signature = headers.get('svix-signature')

    if not svix_id or not svix_timestamp or not svix_signature:
        logger.warning("Missing Svix headers in webhook request.")
        return HttpResponseBadRequest("Missing Svix headers.")

    # Verify webhook signature using Svix
    try:
        wh = Webhook(webhook_secret)
        evt = wh.verify(payload, {
            "svix-id": svix_id,
            "svix-timestamp": svix_timestamp,
            "svix-signature": svix_signature,
        })
    except WebhookVerificationError as e:
        logger.error(f"Webhook signature verification failed: {e}")
        return HttpResponseBadRequest(f"Invalid Webhook signature: {e}")
    except Exception as e:
        logger.error(f"Error during webhook verification: {e}")
        return HttpResponseBadRequest(f"Webhook verification error: {e}")

    # Extract event data
    event_type = evt.get('type')
    event_data = evt.get('data')

    logger.info(f"Received Clerk webhook event: {event_type}")

    # Process event using use case
    try:
        use_case = UserWebhookUseCase()
        use_case.handle_event(event_type, event_data)
        return JsonResponse({
            "status": "success",
            "event_type": event_type,
            "message": f"Event {event_type} processed successfully"
        }, status=200)

    except ValueError as e:
        logger.error(f"Validation error processing Clerk webhook event {event_type}: {e}")
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

    except Exception as e:
        logger.error(f"Error processing Clerk webhook event {event_type}: {e}", exc_info=True)
        return JsonResponse({
            "status": "error",
            "message": "Internal server error processing webhook event"
        }, status=500)
