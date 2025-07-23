import logging
from datetime import datetime

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
