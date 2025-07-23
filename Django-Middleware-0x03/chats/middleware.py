import logging
from datetime import datetime
from django.http import JsonResponse

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
            user = request.user.email  # Or use any field you prefer, like request.user.username
        
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
