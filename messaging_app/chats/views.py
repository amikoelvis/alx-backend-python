from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)
from .permissions import IsUserInConversation  # Import the custom permission

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserInConversation]  # Added custom permission
    authentication_classes = [JWTAuthentication]

    # Add DRF filters for ordering/search
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__email", "participants__first_name", "participants__last_name"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Only show conversations where the logged-in user is a participant"""
        return self.queryset.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        # Ensure the logged-in user is added as a participant when creating a conversation
        serializer.save(participants=[self.request.user])

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participant_ids, always including the logged-in user"""
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participant_ids = serializer.validated_data["participant_ids"]

        # Fetch users
        participants = list(User.objects.filter(user_id__in=participant_ids))

        # Always include the logged-in user if not already in the list
        if request.user not in participants:
            participants.append(request.user)

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """Custom endpoint to send a message in an existing conversation"""
        conversation = self.get_object()
        message_body = request.data.get("message_body")

        if not message_body:
            return Response({"error": "Message body cannot be empty"}, status=400)

        # Create the message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )
        return Response(MessageSerializer(message).data, status=201)


# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("conversation", "sender")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserInConversation]  # Added custom permission
    authentication_classes = [JWTAuthentication]

    # Add DRF filters for searching messages & ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body", "sender__email", "sender__first_name", "sender__last_name"]
    ordering_fields = ["sent_at"]
    ordering = ["-sent_at"]

    def get_queryset(self):
        """
        Only list messages in conversations the user participates in.
        Optional filter: ?conversation=<uuid> to limit to one conversation
        """
        qs = self.queryset.filter(conversation__participants=self.request.user)

        # Optional query param for filtering messages by conversation_id
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            qs = qs.filter(conversation__conversation_id=conversation_id)

        return qs
    
    def perform_create(self, serializer):
        """Create a new message while ensuring the sender is the logged-in user"""
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new message for a conversation"""
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation_id and message_body are required"},
                status=400
            )

        # Get conversation & validate participant
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not part of this conversation"}, status=403)

        # Create the message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )
        return Response(MessageSerializer(message).data, status=201)
