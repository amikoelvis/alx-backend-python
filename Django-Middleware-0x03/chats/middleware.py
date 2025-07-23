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
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Check if the user is authenticated
        user = user.request if request.user.is_authenticated else 'Anonymous'

        # Log the details (timestamp, user, and request path)
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Get the response and return it 
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
