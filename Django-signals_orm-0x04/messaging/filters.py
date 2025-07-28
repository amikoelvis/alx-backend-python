# chats/filters.py
import django_filters
from .models import Message
from django_filters import DateTimeFilter

class MessageFilter(django_filters.FilterSet):
    # Filter by sender email
    sender_email = django_filters.CharFilter(field_name='sender__email', lookup_expr='icontains')

    # Filter messages sent in a date range
    sent_after = DateTimeFilter(field_name='sent_at', lookup_expr='gte', label='Sent After')
    sent_before = DateTimeFilter(field_name='sent_at', lookup_expr='lte', label='Sent Before')

    class Meta:
        model = Message
        fields = ['sender_email', 'sent_after', 'sent_before']
