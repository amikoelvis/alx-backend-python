import logging
from datetime import datetime
from django.http import JsonResponse
from django.core.cache import cache
from time import time

# Setting up logging configuration
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')  # Custom log format
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure 'user' is always defined
        user = 'Anonymous'  # Default to 'Anonymous'
        if request.user.is_authenticated:
            user = request.user.email
        
        # Log the details (timestamp, user, and request path)
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Get the response and return it
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current time
        current_time = datetime.now().hour

        # Restrict access outside 9 PM to 6 PM
        if current_time < 9 or current_time > 18:
            return JsonResponse(
                {"error": "Access to the chat is restricted between 9 PM and 6 PM."},
                status=403
            )

        # Continue processing the request if it's within the allowed hours
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track POST requests (messages)
        if request.method == "POST" and request.path.startswith('/api/messages/'):
            user_ip = self.get_client_ip(request)
            cache_key = f"message_count_{user_ip}"
            current_time = time()

            # Get the existing message count and timestamp from the cache
            message_data = cache.get(cache_key, {"count": 0, "timestamp": current_time})

            # Check if 1 minute has passed since the first message in the window
            if current_time - message_data["timestamp"] > 60:
                message_data = {"count": 0, "timestamp": current_time}

            # Check the current message count
            if message_data["count"] >= 5:
                # If the user exceeded the message limit, return an error response
                return JsonResponse(
                    {"error": "You have exceeded the limit of 5 messages per minute."},
                    status=403
                )

            # Increment the message count
            message_data["count"] += 1
            # Save the updated count back to the cache with a timeout of 1 minute
            cache.set(cache_key, message_data, timeout=60)

        # Proceed with the next middleware or view if within the limit
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get the IP address of the client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check user role for specific actions, e.g., POST requests to send a message
        if request.method == "POST" and request.path.startswith('/api/messages/'):
            user = request.user

            # Check if the user is an admin or moderator
            if not user.is_admin and not user.is_moderator:
                return JsonResponse(
                    {"error": "You do not have permission to perform this action."},
                    status=403
                )

        # Proceed with the next middleware or view
        response = self.get_response(request)
        return response
