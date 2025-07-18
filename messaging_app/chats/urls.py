from django.urls import path, include         # Always import path & include
from rest_framework import routers            # Import DRF routers

from .views import ConversationViewSet, MessageViewSet

# Explicitly create a DRF DefaultRouter instance
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Expose the router-generated URLs
urlpatterns = [
    path('', include(router.urls)),           # This will generate /conversations/ & /messages/
]
