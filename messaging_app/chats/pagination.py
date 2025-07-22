# chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # Set the page size to 20 messages per page
    page_size_query_param = 'page_size'  # Allow clients to change page size
    max_page_size = 100  # Limit maximum page size to 100
