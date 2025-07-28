# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsAuthenticatedAndParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False

        # If the action is related to a specific conversation or message
        if hasattr(view, 'get_object'):
            conversation = view.get_object()
            return request.user in conversation.participants.all()

        # Allow the listing action to proceed as it's not linked to a specific conversation
        return True

    def has_object_permission(self, request, view, obj):
        """
        This method ensures that the user can perform the action only if they are part of the conversation.
        """
        # Only participants can access a specific message or conversation
        if request.user in obj.participants.all():
            if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
                return True

            # Allow modification or deletion (PUT, PATCH, DELETE) only if the user is a participant
            return request.user == obj.sender  # Allow if the user is the sender of the message
        return False
