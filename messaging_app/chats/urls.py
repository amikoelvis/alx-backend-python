from django.urls import path, include            # Explicit import
from rest_framework import routers               # Explicit DRF router import

from .views import ConversationViewSet, MessageViewSet

# Create DRF router instance
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include router-generated URLs
urlpatterns = [
    path('', include(router.urls)),              # All routes from the router
]

# always explicitly include from django.urls import path, include and clearly call routers.DefaultRouter()