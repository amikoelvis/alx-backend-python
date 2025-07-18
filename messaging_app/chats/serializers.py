from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()        # Explicit CharField
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source="sender.email", read_only=True)  # Explicit CharField for sender email
    sender_name = serializers.SerializerMethodField()  # Computed field

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender_email",
            "sender_name",
            "message_body",
            "sent_at",
            "is_read",
        ]

    def get_sender_name(self, obj):
        """Return full sender name for display"""
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()


# Conversation Serializer (Nested Messages)
class ConversationSerializer(serializers.ModelSerializer):
    # Nested participants
    participants = UserSerializer(many=True, read_only=True)

    # Nested messages inside the conversation
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]

    def get_messages(self, obj):
        """Return serialized messages for this conversation"""
        messages_qs = obj.messages.all().order_by("sent_at")
        return MessageSerializer(messages_qs, many=True).data


# Conversation Create Serializer (with validation)
class ConversationCreateSerializer(serializers.Serializer):
    """Create a conversation with a list of participant user_ids"""
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False
    )

    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value
