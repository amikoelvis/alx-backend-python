# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsUserInConversation(permissions.BasePermission):
    """Custom permission to ensure users can only access their own conversations and messages."""
    
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return False

        # If the view is for listing conversations, check if the user is a participant
        if view.action == 'list':
            return request.user in view.get_queryset().first().participants.all()

        # If the view is for a specific conversation or message, ensure user is a participant
        if hasattr(view, 'get_object'):
            conversation = view.get_object()
            return request.user in conversation.participants.all()
        
        return True
