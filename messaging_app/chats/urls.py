from django.urls import path, include                       # Explicit imports
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter  # Nested router

from .views import ConversationViewSet, MessageViewSet

# Main router for conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under a conversation
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Combine both top-level and nested routes
urlpatterns = [
    path('', include(router.urls)),              # /conversations/
    path('', include(conversations_router.urls)) # /conversations/<id>/messages/
]
