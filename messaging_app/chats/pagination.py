# chats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20  # Set the page size to 20
    page_size_query_param = 'page_size'
    max_page_size = 100  # You can set the max page size as needed

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total number of messages
            'next': self.get_next_link(),  # Next page link
            'previous': self.get_previous_link(),  # Previous page link
            'results': data  # The actual messages data
        })
